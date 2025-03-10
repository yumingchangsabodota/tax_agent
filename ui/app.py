import logging

from shiny import App, ui
from shiny.session import get_current_session
from shiny.session import Session

from ui.agent_adapter import AgentAdapter


logger = logging.getLogger("shiny.ui")

adapter = AgentAdapter()


app_ui = ui.page_fillable(
    ui.panel_title("Tax Agent UI"),
    ui.chat_ui("chat"),
    fillable_mobile=True,
)

# Create a welcome message
welcome = ui.markdown(
    """
    Hi! This is a testing chat UI app for Tax Agent.
    Tax Agent is a conversational AI that can help you with your tax-related queries.
    """
)


def server(input, output, session: Session):
    chat = ui.Chat(id="chat", messages=[welcome])

    # Define a callback to run when the user submits a message
    @chat.on_user_submit
    async def _():
        # Get the user's input
        user = chat.user_input()
        # tmp fix for the shiny ui bug for chinese input (Chinese input needs to press return twice)
        chat.update_user_input(value="")

        # Append a response to the chat
        if user == None:
            user = ""
        agent_res = adapter.call_ai(user, session.id)
        logger.debug(f"User: {user} Agent response: {agent_res}")
        agent_output = ui.markdown(agent_res[0])
        await chat.append_message(f"{agent_output}")


app = App(app_ui, server)
