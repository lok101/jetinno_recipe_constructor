from dataclasses import dataclass

from src.adapters.models import DrinkModel, StepModel
from src.domain.entities.machine_drink import MachineDrink
from src.domain.entities.step import BaseStep
from src.domain.entities.vending_machine_profile import VendingMachineProfile
from src.domain.enums import ComponentName, CupType
from src.domain.step_dispatcher import StepsDispatcher
from src.infra.google_sheets_api import GoogleSheetsAPI


@dataclass(frozen=True, slots=True, kw_only=True)
class GetDrinksAdapter:
    step_dispatcher: StepsDispatcher
    gspread_api_client: GoogleSheetsAPI = GoogleSheetsAPI()

    def get_machine_drinks(self, machine_profile: VendingMachineProfile) -> list[MachineDrink]:
        models: list[DrinkModel] = self.gspread_api_client.get_machine_drinks_data(machine_profile.recipe_table_name)

        return [
            self._map_to_domain(model, machine_profile, drink_order)
            for drink_order, model in enumerate(models, 1)
        ]

    def _map_to_domain(self, model: DrinkModel, machine_profile: VendingMachineProfile,
                       drink_order: int) -> MachineDrink:
        steps = [
            self._create_step(step_model, order, machine_profile)
            for order, step_model in enumerate(model.steps, start=1)
        ]

        pic_path: str = f"{machine_profile.model}_{model.id}.png"

        return MachineDrink(
            id=model.id,
            name=model.name,
            is_active=model.is_active,
            capacity=model.capacity,
            cup_type=model.cup_type or CupType.MEDIUM,
            recipe_name=model.name,
            steps=steps,
            order=drink_order,
            price=model.price,
            pic_path=pic_path
        )

    def _create_step(
            self, step_model: StepModel, order: int, machine_profile: VendingMachineProfile
    ) -> BaseStep:
        component_name = self._get_component_name(step_model.name)

        step_class = self.step_dispatcher.get_step_type(component_name)

        step_data = step_model.model_dump()

        component: ComponentName = ComponentName(step_model.name)

        step_data['order'] = order
        step_data['component_name'] = component
        step_data['canister_id'] = machine_profile.get_container_id(component)
        step_data['discharge_speed'] = machine_profile.get_discharge_speed(
            component_name=component,
            component_weight=step_model.component_weight,
            water_volume=step_model.water_volume,
        )

        return step_class.model_validate(step_data)

    @staticmethod
    def _get_component_name(step_name: str) -> ComponentName:
        try:
            return ComponentName(step_name)
        except ValueError:
            raise ValueError(f"Неизвестное имя компонента: '{step_name}'")
