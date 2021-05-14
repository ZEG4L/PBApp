import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

gc = gspread.service_account(filename='mycredentials.json')

gsheet = gc.open("phonebooking-tool")
wsheet = gsheet.worksheet("sheet1")

class PbClient:
    def __init__(self, name, number, address, family_size, delivery_details,
                 neighborhood, baby_needs, pairs_of_bags, default_caller):
        self.name = name
        self.number = number
        self.address = address
        self.family_size = family_size
        self.delivery_details = delivery_details
        self.neighborhood = neighborhood
        self.baby_needs = baby_needs
        self.pairs_of_bags = pairs_of_bags
        self.default_caller = default_caller
    
    def add_to_spreadsheet(self):
        row_data = [self.name, self.number, self.address, self.family_size,
                    self.delivery_details, self.neighborhood, self.baby_needs,
                    self.pairs_of_bags, self.default_caller]
        wsheet.insert_row(row_data, 2)


def retrieve_client_data(client_name):
    df = pd.DataFrame(gsheet.sheet1.get_all_records())
    for index in range(len(df.Name)):
        if(client_name == df.Name[index]):
            return(list(df.loc[index]), index)

def remove_client_data(client_index):
    wsheet.delete_row(client_index)


new_client = PbClient("temp", 9, "420 Wallabe Way", 8, "Coke", "Carlson", "", 5, "Scott")
#new_client.add_to_spreadsheet()
remove_client_data(2)
