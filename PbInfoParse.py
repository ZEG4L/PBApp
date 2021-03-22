# Jinghua Zhang
# 3/21/2021
# This file creates a class struct for phonebankers
# Receive each form submission on slack as an http request and parse information from them
# TESTING: Currently I am using a json file as simulated input and storing the parsed info in a txt file
# REQUIRED LIBRARIES: requests, Flask, json

import requests
import json


# Struct for Phonebanker
class PBInfo:
    def __init__(self, name: str = "Not Provided", contact: str = "", zip_code: int = 0, languages: str = "", firsttime = True):
        self.name = name
        self.contact = contact
        self.zip_code = zip_code
        self.languages = languages
        self.firsttime = firsttime


# Parses json file to a struct
def parsing_information(json_filename: str) -> PBInfo:
    with open(json_filename, 'r') as json_file:
        data = json.load(json_file)
        name = data['state']['values']['name']['input_name']['value']
        contact = data['state']['values']['contact']['input_contact']['value']
        zip_code = data['state']['values']['zip_code']['input_zip']['value']
        raw_str = data['state']['values']['languages']['input_languages']['value']
        language = ""
        for char in raw_str:
            if str.isalpha(char):
                language += char.lower()
        first_time_status = data['state']['values']['first_time']['input_first_time']['selected_options'][0]['text']["text"]
        if "Yes" in first_time_status:
            result = PBInfo(name, contact, zip_code, language, True)
        else:
            result = PBInfo(name, contact, zip_code, language, False)
        return result


# Parsed information can then be sent to Wranglers and used to select call lists
# TEST: Right now it is being written to a file in the current project folder
def writing_information(phonebankers: [PBInfo]) -> None:
    with open("Phonebanker_Info.txt", "w") as pb_info:
        for pb in phonebankers:
            pb_info.write(f"Name: {pb.name}\n")
            pb_info.write(f"Contact: {pb.contact}\n")
            pb_info.write(f"Zip_Code: {pb.zip_code}\n")
            pb_info.write(f"Languages: {pb.languages}\n")
            pb_info.write(f"FirstTime: {pb.firsttime}\n\n")


# Test functions

# TEST Creates a simulated human json file mimicking the body of Slack response
# These will be in the body of "view" section of the http payload
# Reference: https://api.slack.com/reference/interaction-payloads/views
def test_human() -> None:
    human_one = {
        'state': {
            'values': {
                "name": {
                    "input_name": {
                        "value": "John Doe"
                    }
                },
                "contact": {
                    "input_contact": {
                            "value": "9490000000"
                        }
                },
                "zip_code": {
                    "input_zip": {
                        "value": "00000"
                    }
                },
                "languages": {
                    "input_languages": {
                        "value": "English, Spanish"
                    }
                },
                "first_time": {
                    "input_first_time": {
                        "selected_options": [{
                            "text": {
                                    "text": "Yes, I am."
                            }
                        }]
                    }
                }

            }
        }
    }
    human_two = {
        'state': {
            'values': {
                "name": {
                    "input_name": {
                        "value": "Jane Doe"
                    }
                },
                "contact": {
                    "input_contact": {
                        "value": "7140000000"
                    }
                },
                "zip_code": {
                    "input_zip": {
                        "value": "11111"
                    }
                },
                "languages": {
                    "input_languages": {
                        "value": "English/Spanish/Japanese"
                    }
                },
                "first_time": {
                    "input_first_time": {
                        "selected_options": [{
                            "text": {
                                "text": "No, I'm not."
                            }
                        }]
                    }
                }

            }
        }
    }
    with open("human_one.json", 'w') as human_one_json:
        json.dump(human_one,human_one_json)
    with open("human_two.json", 'w') as human_two_json:
        json.dump(human_two,human_two_json)


# Test should create a file called Phonebanker_Info.txt that contains information
def run_test() -> None:
    test_human()
    list_of_pb = [parsing_information("human_one.json"), parsing_information("human_two.json")]
    writing_information(list_of_pb)
    print("Test complete")


if __name__ == "__main__":
    run_test()