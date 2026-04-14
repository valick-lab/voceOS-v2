import sys
import json
import datetime

def process_command(cmd):
    if "hello" in cmd:
        return "Hello ouou"
    elif "time" in cmd:
        return str(datetime.datetime.now())
    else:
        return "Unknown command"

if __name__ == "__main__":
    for line in sys.stdin:
        try:
            data = json.loads(line)
            command = data.get("command", "")

            if not isinstance(command, str):
                command = str(command)

            result = process_command(command)

            print(json.dumps({"response": result}))
            sys.stdout.flush()

        except Exception as e:
            print(json.dumps({"response": f"ERROR: {str(e)}"}))
            sys.stdout.flush()