import streamlit as st
from backend.database import SessionLocal, Chat
import time

# Database session
db_session = SessionLocal()


def show_sidebar():
    st.sidebar.header("🗂️ Manage Conversations")

    # Fetch all conversations from the database
    def get_conversations():
        return db_session.query(Chat).all()

    conversations = get_conversations()
    conversation_names = [c.name for c in conversations]

    # Add new conversation
    new_conversation = st.sidebar.text_input("🆕 Start a new conversation:")
    if st.sidebar.button("Create Conversation"):
        if new_conversation.strip() and new_conversation not in conversation_names:
            new_chat = Chat(name=new_conversation)
            db_session.add(new_chat)
            db_session.commit()
            st.sidebar.success(f"Conversation '{new_conversation}' created!")
            time.sleep(2)
            st.rerun()  # Refresh to show the new chat
            st.session_state.active_conversation = new_conversation
        elif new_conversation in conversation_names:
            st.sidebar.warning("Conversation with this name already exists!")
        else:
            st.sidebar.error("Conversation name cannot be empty.")

    # Select an existing conversation
    selected_conversation = st.sidebar.selectbox(
        "📂 Select a conversation:", options=conversation_names)
    if selected_conversation:
        st.session_state.active_conversation = selected_conversation

    # Delete conversation
    if st.sidebar.button("Delete Conversation"):
        if selected_conversation:
            chat_to_delete = db_session.query(Chat).filter_by(
                name=selected_conversation).first()
            if chat_to_delete:
                db_session.delete(chat_to_delete)
                db_session.commit()
                st.session_state.active_conversation = None
                st.sidebar.success(
                    f"Conversation '{selected_conversation}' deleted!")
                time.sleep(2)
                st.rerun()  # Refresh the page
