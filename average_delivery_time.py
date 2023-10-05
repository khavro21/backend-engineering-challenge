import json
from datetime import datetime, timedelta
from get_datetimes import convert_string_to_datetime
import argparse

def calculate_average_time(input_file: str , window_size: int) -> dict:
    """
    Calculates the average delivery time of all translations for the given ammount of minutes

    :param input_file: The file containing the translations
    :param window_size: The number of past minutes 
    :return: The average time of all translations in last X minutes
    """

    # Get the dicts from file and put them inside a list in json format
    translations_list:list = []
    with open(input_file, "r") as file:
        for line in file:
            translations_list.append(json.loads(line))


    # Removing all the translations that do not match the window_size
    translations_list = filter_translations(translations_list, time_in_minutes=window_size) 
                                  
    translation_durations_in_minute:list = [] # this is needed to calculate the average
    output_list:list = []
    for minute in range(1, window_size + 1):
        for translation in translations_list[:][::-1]:
            if datetime.strptime(translation["timestamp"], "%Y-%m-%d %H:%M:%S") > (datetime.now() - timedelta(minutes=minute)):
                translation_durations_in_minute.append(translation["duration"])
                timestamp = translation["timestamp"]
                translations_list.remove(translation)

        if translation_durations_in_minute:
            # Calculate the average
            average = sum(translation_durations_in_minute) / len(translation_durations_in_minute) 

            # Create output
            translation_output = {"date": timestamp, "average_delivery_time": average}
            output_list.append(translation_output)
        
        # Clear list and timestamp for next minute iteration
        translation_durations_in_minute = []
        timestamp = 0
    
    for item in output_list[::-1]:
        print(item)


def filter_translations(translations:list[dict], time_in_minutes: int) -> list:
    """
    Checks if the translations were made in the required window size.
    Remove the translation from the list if the translation was not done in the required timestamp
    :return filtered translations list
    """
    
    for translation in translations[:]:
        translation_timestamp = convert_string_to_datetime(translation["timestamp"]).replace(second=0, microsecond=0)
        translation["timestamp"] = str(translation_timestamp)
         # Assuming that the duration of the translation in the file is specified in minutes
        if translation_timestamp < (datetime.now() - timedelta(minutes=time_in_minutes)):
            translations.remove(translation)     

    return translations     

   



if __name__ == "__main__":
    # Parsing the arguments
    parser = argparse.ArgumentParser(description="Events Moving Average")
    parser.add_argument("input_file", help="Input file")
    parser.add_argument("window_size", help="Window size")
    args = parser.parse_args()

    input_file = args.input_file
    window_size = int(args.window_size)

    calculate_average_time(input_file=input_file, window_size=window_size)


