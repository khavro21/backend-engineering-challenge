from average_delivery_time import calculate_average_time
from random import randint
from datetime import datetime, timedelta
import io
from contextlib import redirect_stdout
import json
import sys

def test_average_delivery_time():
    """
    Mocking a file(it can be several files for better coverage) and check if the result is expected
    """

    # Given a mocked input file
    with open("delivery_time_test.txt", "w") as file:
        now = datetime.now()
        duration_1 = randint(10, 100)
        duration_2 = randint(10, 100)
        event_1 = {"timestamp": now.strftime("%Y-%m-%d %H:%M:%S.%f"),"translation_id": "random_test_id","source_language": "en","target_language": "fr","client_name": "taxi-eats","event_name": "translation_delivered","nr_words": 100, "duration": duration_1}
        event_2 = {"timestamp": (now + timedelta(minutes=randint(1, 11))).strftime("%Y-%m-%d %H:%M:%S.%f"),"translation_id": "random_test_id","source_language": "en","target_language": "fr","client_name": "taxi-eats","event_name": "translation_delivered","nr_words": 100, "duration": duration_2}
        for event in [event_1, event_2]:
            file.writelines(json.dumps(event) + "\n")
 
    with open("delivery_time_test.txt", "w") as sys.stdout:
        calculate_average_time(input_file="delivery_time_test.txt", window_size=10)

    # When the function runs for that file    
    f = io.StringIO()
    with redirect_stdout(f):
        calculate_average_time(input_file="delivery_time_test.txt", window_size=10)
    out = f.getvalue()

    # Then the result should be the expected one
    ...


