import gspread

from src.models import DrinkModel, ProductModel


def get_google_sheets_data(worksheet_name: str, spreadsheet_name: str = 'Конструктор JL'):
    client = gspread.service_account()
    spreadsheet = client.open(spreadsheet_name)
    worksheet = spreadsheet.worksheet(worksheet_name)
    return worksheet.get_values()[1:]


def get_drinks_data(sheet_name: str = "Напитки") -> list[DrinkModel]:
    headers = ["id", "full_name", "updated", "name", "capacity", "cup_type"]
    data = get_google_sheets_data(sheet_name)

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
            for i in range(0, len(steps), 3) if steps[i] and i + 2 < len(steps)
        ]

        drink_model = DrinkModel.model_validate(drink_data)
        res.append(drink_model)

    return res


def get_products_data(sheet_name: str) -> list[ProductModel]:
    headers = ["visible", "matrix_id", "full_name", "price"]
    data = get_google_sheets_data(sheet_name)

    res = []

    for item in data:
        product_data = dict(zip(headers, item[:len(headers)]))
        product_model = ProductModel.model_validate(product_data)
        res.append(product_model)

    return res
