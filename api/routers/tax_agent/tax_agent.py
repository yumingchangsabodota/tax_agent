
import logging

from datetime import datetime

from fastapi import APIRouter

from langchain_core.messages import HumanMessage

from api.routers.tax_agent.model.message import UserMessage, AIResponse
from src.ai_model.azure_openai import azure_llm_4o_mini_standard
from src.bot.router_agent.agent import LuciusRouterAgent
from src.db.mongo.mongo_connector import mongo_atlas_db

from langgraph.checkpoint.mongodb import MongoDBSaver

from src.db.mongo.chat_session import get_session_thread


logger = logging.getLogger("lucius_router_agent.api")

router = APIRouter()

checkpointer = MongoDBSaver(mongo_atlas_db)
smart_agent = LuciusRouterAgent(
    azure_llm_4o_mini_standard, checkpointer=checkpointer)


@router.post("/")
async def call(user_input: UserMessage) -> AIResponse:

    current_date = datetime.today().strftime(format="%Y-%m-%d")
    session_id = user_input.session_id
    email = user_input.user_email
    thread_count = get_session_thread(session_id, email, current_date)

    thread_id = f"{session_id}_{current_date}_{thread_count}"
    thread = {"configurable": {"thread_id": thread_id,
                               "user_email": email}}

    logger.info(
        f"Session({thread_id}) User({user_input.user_email}) sent message: {user_input.message}")
    messages = [HumanMessage(user_input.message)]

    logger.info(messages)
    result = smart_agent.graph.invoke({"messages": messages,
                                       "user_email": email,
                                       "session_id": session_id,
                                       "date": current_date,
                                       "thread_count": thread_count},
                                      thread)

    return AIResponse(message=result["messages"][-1].content, session_id=user_input.session_id)
