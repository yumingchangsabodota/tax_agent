
import logging

from datetime import datetime

from fastapi import APIRouter

from langchain_core.messages import HumanMessage

from api.routers.tax_agent.model.message import UserMessage, AIResponse
from agent.tax_agent import TaxAgent

from langgraph.checkpoint.mongodb import MongoDBSaver

from db.mongo.mongo_connector import mongo_atlas_db


logger = logging.getLogger("tax_agent.api")

router = APIRouter()

checkpointer = MongoDBSaver(mongo_atlas_db)
smart_agent = TaxAgent(checkpointer)


@router.post("/")
async def call(user_input: UserMessage) -> AIResponse:

    session_id = user_input.session_id

    thread = {"configurable": {"thread_id": session_id}}

    logger.info(
        f"Session({session_id}) sent message: {user_input.message}")
    messages = [HumanMessage(user_input.message)]

    logger.info(messages)
    result = smart_agent.graph.invoke({"messages": messages},
                                      thread)

    return AIResponse(message=result["messages"][-1].content, session_id=user_input.session_id)
