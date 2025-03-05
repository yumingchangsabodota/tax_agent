
import logging

from datetime import datetime

from fastapi import APIRouter

from langchain_core.messages import HumanMessage

from api.routers.tax_agent.model.message import UserMessage, AIResponse
from agent.tax_agent import TaxAgent


logger = logging.getLogger("tax_agent.api")

router = APIRouter()

smart_agent = TaxAgent()


@router.post("/")
async def call(user_input: UserMessage) -> AIResponse:

    current_date = datetime.today().strftime(format="%Y-%m-%d")
    session_id = user_input.session_id

    thread = {"configurable": {"thread_id": session_id}}

    logger.info(
        f"Session({session_id}) sent message: {user_input.message}")
    messages = [HumanMessage(user_input.message)]

    logger.info(messages)
    result = smart_agent.graph.invoke({"messages": messages},
                                      thread)

    return AIResponse(message=result["messages"][-1].content, session_id=user_input.session_id)
