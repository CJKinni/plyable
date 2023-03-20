from plyable import Plyable
import sys
import json

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} filename")
    sys.exit(1)

filename = sys.argv[1]
source = open(filename, 'r').read()

session = Plyable()
session.system_message =  """
You are a code review bot.
You will be given a complete code file.

You must return a JSON object formatted as follows:

{
    "errors": ["line 1: missing semicolon"],
    "suggestions": ["line 3: use a for loop instead of a while loop"],
    "code": "print(\\\"hello world\\\");\\nprint(\\\"hello world\\\", \\\"hello world\\\");\\nfor i in range(10):\\n    print(i)"
}

Do not include anything else in your response.
Your response must be valid JSON.
You must not return any other output.
The first line of your response must be a '{' character.
The last line of your response must be a '}' character.
"""

@Plyable.validate_output_message
def validate_json(self, message):
    try:
        j = json.loads(message)
    except:
        error = "Response is not valid JSON, return a valid JSON object."
        print(error)
        print(message)
        return (False, error)

    expected_keys = ['errors', 'suggestions', 'code']
    for key in expected_keys:
        if key not in j:
            error = f"Output is missing the '{key}' key, return a valid JSON object."
            print(error)
            print(message)
            return (False, error)

response = session.send(f"filename: {filename}\n\n```\n{source}\n```")
print(response)
print('---')
print(json.loads(response)['code'])