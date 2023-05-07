import streamlit as st
from streamlit_chat import message
import os
import requests
from dataclasses import dataclass


@dataclass
class Message:
    is_user: bool
    message: str


class ChatAPIError(Exception):
    pass


CHAT_API_URL = os.environ.get("CHAT_API_URL")

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []


def ui():
    st.set_page_config(page_title="Streamlit Chat - Demo", page_icon=":robot:")
    st.header("Streamlit Chat - Demo")

    # ユーザーの入力待ち
    input_text = st.text_input("You: ", "Hello, how are you?", key="input")
    if input_text:
        res = send_chat_message(text=input_text)

        # ユーザーの質問、回答結果をインメモリに保存
        st.session_state["chat_history"].append(
            Message(is_user=True, message=input_text)
        )
        st.session_state["chat_history"].append(Message(is_user=False, message=res))

    # チャット履歴を表示
    if st.session_state["chat_history"]:
        for message_data in st.session_state["chat_history"]:
            message(message=message_data.message, is_user=message_data.is_user)


def send_chat_message(text: str) -> str:
    res = requests.post(url=CHAT_API_URL, json={"message": text})
    if res.status_code != 200:
        res.raise_for_status()

    return res.json()["message"]


if __name__ == "__main__":
    ui()
