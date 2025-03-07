
import logging

from typing import TypedDict, Annotated, List, Any, Tuple


from langchain_core.tools import tool
from langchain_core.messages import AnyMessage, SystemMessage, ToolMessage, trim_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph, START

from agent.sys_prompt import SYS_PROMPT
from agent.message_reducer import reduce_messages
from ai_model.openai_model import openai_4o_mini

from db.mongo.tax_doc_vector_store import vector_store


logger = logging.getLogger("tax_agent")


@tool
def retrieve_tax_category_info(query: str) -> str:
    """Useful tool to retrieve tax category based on user input"""
    logger.debug("-----retrieve_tax_category_info-----")
    logger.debug(f"Query: {query}")
    results = vector_store.similarity_search(query=query,
                                             k=3)
    possible_categories = []
    for i in range(len(results)):
        logger.debug(results[i])
        possible_categories.append(f"Page {i+1}\n" + results[i].page_content)
    possible_categories = "\n\n".join(possible_categories)
    logger.debug(
        "Possible answer is in one of the below pages:\n" + possible_categories)
    logger.debug("-----retrieve_tax_category_info-----")
    return {"message": "Possible answer is in one of the below pages:\n" + possible_categories}


class TaxAgentState(TypedDict):
    messages: Annotated[List[AnyMessage], reduce_messages]


class TaxAgent:
    def __init__(self, checkpointer: MemorySaver = None):
        tools = [
            retrieve_tax_category_info
        ]
        self.checkpointer = checkpointer
        self.tools = {t.name: t for t in tools}

        graph = StateGraph(TaxAgentState)

        graph.add_node("llm_node", self.llm_node)
        graph.add_node("tool_node", self.tool_node)

        graph.add_edge(START, "llm_node")
        graph.add_conditional_edges("llm_node",
                                    self.next_node,
                                    {"tool_node": "tool_node",
                                     END: END})
        graph.add_edge("tool_node", "llm_node")

        self.graph = graph.compile(checkpointer=checkpointer)
        self.model = openai_4o_mini.bind_tools(tools)

    def llm_node(self, state: TaxAgentState):
        messages = state["messages"]
        inquiry_system_prompt = SystemMessage(
            content=SYS_PROMPT)

        messages = [inquiry_system_prompt] + messages
        messages = self.__trim_messages(messages)
        messages = self.model.invoke(messages)

        return {"messages": [messages]}

    def tool_node(self, state: TaxAgentState):
        tool_calls = state['messages'][-1].tool_calls
        results = []
        for t in tool_calls:
            logger.debug("-----tool_node-----")
            logger.debug(t)
            tool_response = self.tools[t['name']].invoke(t['args'])
            results.append(ToolMessage(tool_call_id=t['id'],
                                       name=t['name'],
                                       content=tool_response["message"]))

            logger.debug("-----tool_node-----")
        return {"messages": results}

    def next_node(self, state: TaxAgentState):
        message = state['messages'][-1]
        if len(message.tool_calls) > 0:
            return "tool_node"
        return END

    def __trim_messages(self, messages: List[AnyMessage]) -> List[AnyMessage]:
        return trim_messages(messages=messages,
                             max_tokens=25000,
                             token_counter=openai_4o_mini,
                             include_system=True,
                             end_on=["human", "tool"],
                             start_on="human"
                             )
