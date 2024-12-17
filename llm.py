# https://platform.openai.com/docs/api-reference/chat

import requests
import os
import json
import tool

endpoint = "https://api.openai.com/v1/chat/completions"

def headers():
    return {
        'Authorization': 'Bearer ' + os.environ['OPENAI_API_KEY'],
        'Content-Type': 'application/json',
    }

def reset(thread):
    return tool.reset(thread)

def invoke(thread):
    content = None
    count = 0
    bench = tool.open()
    tool_messages = []

    while not content and count < 10:
        count += 1
        model = thread["tools"]["model"]
        message = requests.post(
            endpoint,
            headers = headers(),
            json = {
                "model": model["model"],
                "temperature": model["temperature"],
                "messages": thread["messages"] + tool_messages,
                "tools": bench,
                "tool_choice": "auto"
            }).json()["choices"][0]["message"]

        content = message.get("content")

        if not content:
            tool_messages.append(message)

            for call in message.get("tool_calls", []):
                fn = call["function"]
                name = fn["name"]
                args = json.loads(fn["arguments"])
                args["thread"] = thread

                try:
                    output = tool.run(name, args)
                except Exception as e:
                    output = str(e)

                print(f"{name}:")

                if name in ['json']:
                    content = output
                    break
                else:
                    del args["thread"]

                    [print(arg) for arg in args.values()]
                    print(f"\n{output}\n")

                    if name == "digest":
                        tool_messages.clear()

                    tool_messages.append({
                        "role": "tool",
                        "tool_call_id": call["id"],
                        "name": name,
                        "content": output
                    })

    tool.close()
    return content or "Could you rephrase that, please?"

def mini(query):
    try:
        return requests.post(
            endpoint,
            headers = headers(),
            json = {
                "model": "gpt-4o-mini",
                "temperature": 0,
                "messages": [{"role": "user", "content": query[:8000]}]
            }).json()["choices"][0]["message"]["content"]
    except:
        return "Could you rephrase that, please?"
