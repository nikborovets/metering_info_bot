from pprint import pprint
import httplib2
import googleapiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from typing import List, Tuple, Any
from dotenv import load_dotenv, find_dotenv
import os
load_dotenv(find_dotenv())

credentials_file = 'creds.json'
spreadsheet_id = os.getenv('SPREADSHEET_ID')
googlesheets_link = os.getenv('GOOGLESHEETS_LINK')

class GoogleSheetsHandler:
    def __init__(self, credentials_file, spreadsheet_id):
        self.credentials_file = credentials_file
        self.spreadsheet_id = spreadsheet_id
        self.service = self.authorize()

    def authorize(self):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            self.credentials_file,
            ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        )
        http_auth = credentials.authorize(httplib2.Http())
        return googleapiclient.discovery.build('sheets', 'v4', http=http_auth)

    def read_data(self, sheet_name, range_name, majorDimension):
        full_range = f'{sheet_name}!{range_name}'
        # majorDimension = 'ROWS'
        values = self.service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id,
            range=full_range,
            majorDimension=majorDimension
        ).execute()
        return values

    # def write_data_local_calculation(self, sheet_name: str, range_name: str, data_list: List[List[Any]], majorDimension: str):
    #     full_range = f'{sheet_name}!{range_name}'
    #     start_row = int(range_name.split(':')[0][1:])
    #     body = {
    #         "valueInputOption": "USER_ENTERED",
    #         "data": [
    #             {
    #                 "range": full_range,
    #                 "majorDimension": majorDimension,
    #                 "values": data_list,
    #             },
    #         ]
    #     }
    #     values = self.service.spreadsheets().values().batchUpdate(
    #         spreadsheetId=self.spreadsheet_id,
    #         body=body
    #     ).execute()

    def write_data_with_calculating_in_the_table(self, sheet_name: str, data_coordinates: List[Tuple[str, int]], data_list: List[Any], majorDimension: str):
        body = {
            "valueInputOption": "USER_ENTERED",
            "data": []
        }
        for i, (col, row) in enumerate(data_coordinates):
            body["data"].append({
                "range": f"{sheet_name}!{col}{row}:{col}{row}",
                "majorDimension": "ROWS",
                "values": [[data_list[i]]],
                # "userEnteredFormat": {
                # "textFormat": {
                #     "fontFamily": 'Arial',
                #     "fontSize": 11,
                #     }
                # }
            })
        print(body['data'])
        values = self.service.spreadsheets().values().batchUpdate(
            spreadsheetId=self.spreadsheet_id,
            body=body
        ).execute()

        

if __name__ == "__main__":

    sheets_handler = GoogleSheetsHandler(credentials_file, spreadsheet_id)


    sheet_name = 'flat0'


    read_range = 'A1:P50'
    read_values = sheets_handler.read_data(sheet_name, read_range, 'ROWS')
    print(read_values['values'][18], '\n\n', len(read_values['values']))
   


    # data_list_to_write = [['1', 'John Doe', '500', '20.02.2023'],
    #                       ['2', 'Jane Smith', '600', '21.02.2023'],
    #                       ['3', 'Ivan Ivanov', '700', '22.02.2023']]
    
    # start_row = 1
    # write_range = f'A{start_row}:D{start_row + len(data_list_to_write)}'


    # sheets_handler.write_data(sheet_name, write_range, data_list_to_write)


    # data_list_to_write1 = [['твтвдв', 'твтвьдва', 'воовлу']]
    # len_columns = 5
    # start_row = len_columns + 1
    # write_range = f'A{start_row}:C{start_row}'
    # sheets_handler.write_data('flat1', write_range, data_list_to_write1, 'ROWS')
    # print(type(data_list_to_write1))

