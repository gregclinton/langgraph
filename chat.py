import llm
from dotenv import load_dotenv
from datetime import datetime

def reset(thread):
    thread["messages"] = []
    thread["runs"] = []
    return llm.reset(thread)

def back(thread):
    del thread["messages"][thread["runs"].pop():]

def run(prompt, thread):
    def message(role, content):
        if role != "system":
            print(f"{role}:\n{content}\n", flush=True)
        return { "role": role, "content": content }

    load_dotenv("keys")
    thread["runs"].append(len(thread["messages"]))
    messages = thread["messages"]
    messages.append(message("user", prompt))
    use = open("docs/use").read().split(",")
    docs = "\n\n".join(open(f"docs/{doc}").read() for doc in use)
    docs = docs.replace("{today}", datetime.now().strftime("%B %d, %Y"))
    docs = [message("system", docs)]
    reply = llm.invoke(docs + messages, thread)
    messages.append(message("assistant", reply))
    return reply
