
from uuid import uuid4
from langchain_core.messages import AnyMessage


def reduce_tool_calls(messages: list[AnyMessage]) -> list[AnyMessage]:
    for m in range(len(messages)):
        if hasattr(messages[m], "tool_calls") and len(messages[m].tool_calls) > 0:
            reduced_tool_calls = {}
            for i in range(len(messages[m].tool_calls)):
                if messages[m].tool_calls[i]["name"] not in reduced_tool_calls:
                    reduced_tool_calls[messages[m].tool_calls[i]
                                       ["name"]] = messages[m].tool_calls[i]
            messages[m].tool_calls = list(reduced_tool_calls.values())
    return messages


def reduce_messages(left: list[AnyMessage], right: list[AnyMessage]) -> list[AnyMessage]:
    # assign ids to messages that don't have them
    for message in right:
        if not message.id:
            message.id = str(uuid4())
    # merge the new messages with the existing messages
    merged = left.copy()
    for message in right:
        for i, existing in enumerate(merged):
            # replace any existing messages with the same id
            if existing.id == message.id:
                merged[i] = message
                break
        else:
            # append any new messages to the end
            merged.append(message)
    merged = reduce_tool_calls(merged)
    return merged


__all__ = ["reduce_messages"]
