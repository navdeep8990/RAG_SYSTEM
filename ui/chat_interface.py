import streamlit as st
from backend.database import SessionLocal, Chat
from backend.helpers import create_knowledge_base_from_pdf, create_knowledge_base_from_url
from backend.llm_setup import llm
from langchain.chains import RetrievalQA
import time
import os

# Database session
db_session = SessionLocal()


def show_chat_interface():
    if st.session_state.get("active_conversation"):
        # Fetch the selected conversation
        active_chat = db_session.query(Chat).filter_by(
            name=st.session_state.active_conversation).first()

        st.header(f" 💬 Chat - {st.session_state.active_conversation}")

        # Display the current knowledge base references with delete buttons
        knowledge_base_deleted = False

        if active_chat.knowledge_base_ref_pdf and active_chat.knowledge_base_ref_url:
            st.subheader("📚 Knowledge Base: PDF and URL")
            st.markdown(
                f"- PDF: {os.path.basename(active_chat.knowledge_base_ref_pdf)}")
            if st.button("Delete PDF"):
                active_chat.knowledge_base_ref_pdf = None
                db_session.commit()
                knowledge_base_deleted = True
                st.success("PDF knowledge base deleted!")

            st.markdown(f"- URL: {active_chat.knowledge_base_ref_url}")
            if st.button("Delete URL"):
                active_chat.knowledge_base_ref_url = None
                db_session.commit()
                knowledge_base_deleted = True
                st.success("URL knowledge base deleted!")
        elif active_chat.knowledge_base_ref_pdf:
            st.subheader("📚 Knowledge Base: PDF")
            st.markdown(
                f"- PDF: {os.path.basename(active_chat.knowledge_base_ref_pdf)}")
            if st.button("Delete PDF"):
                active_chat.knowledge_base_ref_pdf = None
                db_session.commit()
                knowledge_base_deleted = True
                st.success("PDF knowledge base deleted!")
        elif active_chat.knowledge_base_ref_url:
            st.subheader("📚 Knowledge Base: URL")
            st.markdown(f"- URL: {active_chat.knowledge_base_ref_url}")
            if st.button("Delete URL"):
                active_chat.knowledge_base_ref_url = None
                db_session.commit()
                knowledge_base_deleted = True
                st.success("URL knowledge base deleted!")
        else:
            st.warning("No knowledge base available for this conversation.")

        # Handle File and URL upload based on the current state of the knowledge base
        if not active_chat.knowledge_base_ref_url:
            url = st.text_input("Enter a URL")
            if st.button("Add URL"):
                if url.strip():
                    with st.spinner("Processing URL..."):
                        active_chat.knowledge_base_ref_url = url
                        db_session.commit()
                        st.success(f"Web knowledge base created from URL!")
                        time.sleep(2)
                        st.rerun()
                else:
                    st.warning("URL cannot be empty.")
        if not active_chat.knowledge_base_ref_pdf:
            uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
            if uploaded_file:
                with st.spinner("Processing PDF..."):
                    file_path = f"data/knowledge_base/{uploaded_file.name}"
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    active_chat.knowledge_base_ref_pdf = file_path
                    db_session.commit()
                    st.success(
                        f"PDF knowledge base '{uploaded_file.name}' created!")
                    time.sleep(2)
                    st.rerun()

        # Reload the knowledge base after page refresh
        knowledge_base = None
        if active_chat.knowledge_base_ref_pdf:
            knowledge_base = create_knowledge_base_from_pdf(
                active_chat.knowledge_base_ref_pdf)
        elif active_chat.knowledge_base_ref_url:
            knowledge_base = create_knowledge_base_from_url(
                active_chat.knowledge_base_ref_url)

        # Create retriever and QA chain
        if knowledge_base:
            retriever = knowledge_base.as_retriever(search_kwargs={"k": 3})
            qa_chain = RetrievalQA.from_chain_type(
                llm=llm, retriever=retriever)

            # Display chat messages
            # Load JSON-encoded history
            chat_history = eval(active_chat.history)
            for chat in chat_history:
                with st.chat_message(chat["role"]):
                    st.markdown(chat["content"])

            # Chat input
            user_input = st.chat_input("Ask your question:")
            if user_input:
                # Append user message to chat history
                chat_history.append({"role": "user", "content": user_input})
                active_chat.history = str(chat_history)  # Save updated history
                db_session.commit()
                with st.chat_message("user"):
                    st.markdown(user_input)

                # Generate and append assistant response
                with st.spinner("Fetching answer..."):
                    response = qa_chain.invoke(user_input)

                # Check if the response contains relevant information
                if response['result'].strip():
                    chat_history.append(
                        {"role": "assistant", "content": response['result']})
                    active_chat.history = str(chat_history)
                    db_session.commit()
                    with st.chat_message("assistant"):
                        st.markdown(response['result'])
        else:
            st.warning(
                "Please upload a file or provide a URL to create a knowledge base.")
    else:
        st.warning(
            "No conversation selected. Please create or select a conversation.")
