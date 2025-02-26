import os
import requests

from typing import Tuple

AGENT_URL: str = os.environ.get('AGENT_URL', 'http://localhost:8087')
POC_AUTH_KEY: str = os.environ.get('POC_AUTH_KEY', '')


class AgentAdapter:
    def __init__(self):
        self.url = AGENT_URL
        self.auth_key = POC_AUTH_KEY
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': POC_AUTH_KEY
        }

    def call_ai(self, msg: str, user_email: str, session_id: str) -> Tuple[str, str]:

        body = {
            "message": msg,
            "user_email": user_email,
            "session_id": session_id
        }

        response = requests.post(
            f"{self.url}/ticket-helper/call", headers=self.headers, json=body)
        response = response.json()

        return response['message'], response['session_id']
