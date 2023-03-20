from plyable import Plyable
import sys
import json

if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} filename")
    sys.exit(1)

filename = sys.argv[1]
source = open(filename, 'r').read()

# Get input until user puts 'EOF' on a line by itself
bug_message = ""
while True:
    in_message = input('')
    if in_message == 'EOF':
        break
    bug_message += in_message

session = Plyable()
session.gpt_version = 'gpt-4'
session.system_message =  """
You are a code review bot.
You will be given an error message, and the code that caused the error.
Explain the error, and suggest a fix.
"""

print(session.send(f"filename: {filename}\n\n```\n{source}\n``` Error message:\n```\n{bug_message}\n```\n"))