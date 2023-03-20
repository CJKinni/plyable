from plyable import Plyable
import plyable.helpers
import time
import json

session = Plyable()
session.system_message =  """
You are a chat therapist.
You will be sent messages from a user in a JSON format like so:

{
    "message": "Hello, how are you?",
    "seconds_to_respond": 3.8452117443084717
}

seconds_to_respond is the number of seconds it took the user to respond to the message.

You must return a JSON object formatted as follows:

{
    "message": "I'm doing well, how are you?",
    "severity": 0.3,
}

Severity is a number between 0 and 1, where 0 is not concerning and 1 is very concerning.
A Human will monitor responses and will intervene if the severity is too high.

Do not include anything else in your response.
Your response must be valid JSON.
You must not return any other output.
The first line of your response must be a '{' character.
The last line of your response must be a '}' character.
"""

@Plyable.validate_input_message
def check_in_json(self, message):
    return plyable.helpers.validate_json(message, ['message', 'seconds_to_respond'], log=True)

@Plyable.validate_output_message
def check_out_json(self, message):
    return plyable.helpers.validate_json(message, ['message', 'severity'], log=True)


while True:
    try:
        start_time = time.time()
        in_message = input(">> ")
        response = session.send(
            json.dumps({
                "message": in_message,
                "seconds_to_respond": time.time() - start_time
            })
        )
        print(response) # This is the response from the model, in JSON format
    except KeyboardInterrupt:
        break