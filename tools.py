import llm
import catalog
import messages
from messages import Message

def call_tool(tool, text):
    if tool == "Catalog":
        return "Sorry, it is not in our catalog."
    return "???"

def invoke(tool, msgs):
    # First determine which tool msgs have not been answered.
    # Then for these, print out completion string consisting of tool answers with To: msg.sender From: tool and body answer
    unanswered = []
    answers = []

    for msg in msgs:
        if msg.recipient == tool:
            unanswered.append(msg)
            break

    for msg in unanswered:
        answers.append(Message(tool, msg.sender, call_tool(tool, msg.body)))

    return messages.to_string(answers) if answers else ""

