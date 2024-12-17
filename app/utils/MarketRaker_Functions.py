import csv
from app.Schemas.MarketDirection_Schema import RequestBody


def get_info_from_csv(file_path,type:str):
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        csv_output = []

        for row in csv_reader:
            csv_output.append(float(row[f"{type}"]))
        return csv_output
    


def format_to_market_direction_format(csv_path:str ,currency:str ):
    output_dict = RequestBody(
        open = get_info_from_csv(csv_path,"open_price"),
        close = get_info_from_csv(csv_path,"close"),
        high = get_info_from_csv(csv_path,"high"),
        low = get_info_from_csv(csv_path,"low"),
        volume = get_info_from_csv(csv_path,"volume")
        )
    return {currency:output_dict.to_dict()}
