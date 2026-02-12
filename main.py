from src.adapters.get_machine_products import GetDrinksAdapter
from src.adapters.save_containers_configuration import SaveContainersConfigurationAdapter
from src.adapters.save_drinks_to_file import SaveDrinksAsRecipesPackAdapter, SaveDrinkAsProductPackAdapter
from src.app import Application
from src.domain.entities.step import CoffeeStep, WaterStep, PowderStep, SugarStep, ColdPowderStep
from src.domain.enums import MachineModel, ComponentName
from src.domain.step_dispatcher import StepsDispatcher
from settings.vending_machines_settings import MachineProfilesSettings

step_dispatcher = StepsDispatcher()

step_dispatcher.register_component(ComponentName.COFFEE, CoffeeStep)
step_dispatcher.register_component(ComponentName.WATER, WaterStep)
step_dispatcher.register_component(ComponentName.MILK, PowderStep)
step_dispatcher.register_component(ComponentName.CHOCO, PowderStep)
step_dispatcher.register_component(ComponentName.VANILLA, PowderStep)
step_dispatcher.register_component(ComponentName.SUGAR, SugarStep)
step_dispatcher.register_component(ComponentName.RAF, PowderStep)

step_dispatcher.register_component(ComponentName.RAF_BANAN, PowderStep)
step_dispatcher.register_component(ComponentName.RAF_CARAMEL, PowderStep)

step_dispatcher.register_component(ComponentName.VANILLA_MILKSHAKE, ColdPowderStep)



profiles = MachineProfilesSettings()

app = Application(
    drinks_data_port=GetDrinksAdapter(
        step_dispatcher=step_dispatcher
    ),
    recipes_constructor=SaveDrinksAsRecipesPackAdapter(),
    products_constructor=SaveDrinkAsProductPackAdapter(),
    save_canister_config=SaveContainersConfigurationAdapter()
)
app.run(machine_model=MachineModel.JL28)

pass
