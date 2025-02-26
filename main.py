import streamlit as st
from ui.sidebar import show_sidebar
from ui.chat_interface import show_chat_interface

# Streamlit UI setup
st.set_page_config(page_title="Multi-Agent Retrieval ",
                   page_icon=":books:", layout="wide")
st.title("🤖 Multi-Agent Retrieval")

# Sidebar management
show_sidebar()

# Chat interface
show_chat_interface()
