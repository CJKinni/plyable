# Plyable Python

A Python microframework for interacting with OpenAI's chat APIs.

## Installing

Install and update using [pip](https://pip.pypa.io/en/stable/quickstart/):

```bash
$ pip install plyable
```

Currently, the only API supported is OpenAI's chat API.  You will need to [sign up for an OpenAI account](https://beta.openai.com/), and [create an API key](https://beta.openai.com/account/api-keys).

Once you have your key, you can set it as the OPENAI_API_KEY environment variable, or you can pass it to the Plyable constructor.

```bash
$ export OPEN_API_KEY="your-key-here"
```

## A Simple Example

```python
from plyable import Plyable

session = Plyable()

while True:
    in_message = input(">> ")
    print("<< " + session.send(in_message))
```

```bash
$ python bot.py
>> Hello, how are you?
<< Hello! As an AI language model, I do not have personal emotions, but I am functioning properly and ready to assist you. How may I help you today?
>>
```

## JSON input and output evaluation

Plyable provides a decorator to validate input and output messages. This decorator will check that the message is valid JSON, and that it contains the specified keys. If the message is not valid, it will be logged, and the LLM will be sent an explanation of the error, and will be asked to retry.  This retry loop will occur up to a specified retry limit (3 by default.)

```python
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
```

## An overview of the Plyable class

The Plyable class is the main class for interacting with the chat API.  It provides methods for sending messages, and for receiving responses.  It also provides a few helper methods for interacting with the API.

### Callbacks

Plyable allows you to specify four callbacks:

 - `on_input_message`
 - `on_output_message`
 - `validate_input_message`
 - `validate_output_message`

The `on_input_message` and `on_output_message` callbacks are called after a message is sent or received.  They are passed the message as a string, and return None. They are useful for logging messages, or for performing other actions on messages.

The `validate_input_message` and `validate_output_message` callbacks are called before a message is sent or received.  They are passed the message as a string, and return a tuple. The tuple is of the form `(bool, str)`.  The first element of the tuple is a boolean indicating whether the message is valid.  The second element is a string containing an error message, if the message is not valid.  These callbacks are useful for validating messages.  If a message is not valid, the LLM will be sent the error messages of all failed validations, and will be asked to retry.  This retry loop will occur up to a specified retry limit (3 by default.)

### Variables

There are a few main variables you might want to modify:

 - `system_message` (default "You are a chat bot"): This is the message that will be sent to the LLM when the session is started.  The system message helps set the behavior of the assistant.
 - `retries` (default 3) This is the number of times the LLM will be asked to retry if the message is not valid.
 - `gpt_version` (default `gpt-3.5-turbo`) Currently only `gpt-3.5-turbo` and `gpt-4` are supported.
 - `rate_limit_retry_enabled` (default `True`) If True, the client will retry if it receives a rate limit error.
 - `rate_limit_retry_timeout` (default `25`) The number of seconds to wait before retrying if a rate limit error is received.
 - `rate_limit_retries` (default `5`) The number of times to retry if a rate limit error is received.

### Methods

#### `send(message)`

Sends a message (string) to the LLM.  Returns the response from the LLM as a string.

LLMs may return data in a particular format.  Currently, this response will only include the content of the message, and will not include any other metadata.  This may change in the future.

To access the entire log, with all metadata, you can access the `message_log` variable.

#### `update_openai_api_key(key)`

Sets the OpenAI API key to the specified key.

## License

This project is licensed under the terms of the AGPLv3 license.
