from dataclasses import dataclass

import gspread

from src.adapters.models import DrinkModel

STEP_BLOCK_SIZE = 4


@dataclass(frozen=True, slots=True)
class GoogleSheetsAPI:
    account = gspread.service_account()

    def _get_google_sheets_data(self, worksheet_name: str, spreadsheet_name: str = 'Конструктор JL'):
        spreadsheet = self.account.open(spreadsheet_name)
        worksheet = spreadsheet.worksheet(worksheet_name)
        return worksheet.get_values()[1:]

    def get_machine_drinks_data(self, sheet_name: str) -> list[DrinkModel]:
        headers = ["is_active", "id", "name", "drink_name", "capacity", "price", "cup_type", "all_water"]
        data = self._get_google_sheets_data(sheet_name)

        res = []

        for item in data:
            drink_data = dict(zip(headers, item[:len(headers)]))

            steps = item[len(headers):]
            drink_data["steps"] = [
                {
                    "name": steps[i],
                    "component_weight": steps[i + 1],
                    "water_volume": steps[i + 2],
                }
                for i in range(0, len(steps), STEP_BLOCK_SIZE) if steps[i] and i + 2 < len(steps)
            ]

            drink_data["is_active"] = True if drink_data["is_active"] == "TRUE"  else False

            drink_model = DrinkModel.model_validate(drink_data)
            res.append(drink_model)

        return res
