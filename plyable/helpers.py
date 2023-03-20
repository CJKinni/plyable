import json

def validate_json(message, expected_keys=[], log=None):
    try:
        j = json.loads(message)
    except:
        error = "Response is not valid JSON, return a valid JSON object."
        if log:
            print(error)
            print(message)
        return (False, error)

    for key in expected_keys:
        if key not in j:
            error = f"Output is missing the '{key}' key, return a valid JSON object."
            if log:
                print(error)
                print(message)
            return (False, error)
