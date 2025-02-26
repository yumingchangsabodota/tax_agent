import logging

from shiny import App, ui
from shiny.session import get_current_session
from shiny.session import Session

from ui.agent_adapter import AgentAdapter

logger = logging.getLogger("shiny.ui")

adapter = AgentAdapter()


app_ui = ui.page_fillable(
    ui.panel_title("Lucius Agent UI"),
    ui.chat_ui("chat"),
    fillable_mobile=True,
)

# Create a welcome message
welcome = ui.markdown(
    """
    Hi! This is a testing chat UI app for Lucius Agent.
    Lucius Agent is an asistant that helps user to figure out what tickets they need to submit, collect all the necessary information and submit the ticket for them.
    [Check Lucius Code Base](https://adc.github.trendmicro.com/Corp-IT/lucius).
    """
)


def server(input, output, session: Session):
    chat = ui.Chat(id="chat", messages=[welcome])

    # Define a callback to run when the user submits a message
    @chat.on_user_submit
    async def _():
        # Get the user's input
        user = chat.user_input()

        # Append a response to the chat
        if user == None:
            user = ""
        agent_res = adapter.call_ai(user, session.id, session.id)
        logger.debug(f"User: {user} Agent response: {agent_res}")
        agent_output = ui.markdown(agent_res[0])
        await chat.append_message(f"{agent_output}")


app = App(app_ui, server)
