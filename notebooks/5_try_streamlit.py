## Prerequisits:
# pip install streamlit
# pip install streamlit-chat  # For chat interface components
# pip install langchain

import streamlit as st
from streamlit_chat import message
import tempfile

from langchain.document_loaders.csv_loader import CSVLoader

if __name__ == '__main__':
    # Set the title for the Streamlit app
    st.title("Chat CSV - 🦜🦙")

    # Create a file uploader in the sidebar
    uploaded_file = st.sidebar.file_uploader("Upload File", type="csv")

    # Handle file upload
    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name

            # Load CSV data using CSVLoader
            loader = CSVLoader(file_path=tmp_file_path, encoding="utf-8", csv_args={'delimiter': ','})
            data = loader.load()

        # Function for conversational chat
        def conversational_chat(query):
            result = query + "!"
            st.session_state['history'].append((query, result))
            return result

        # Initialize chat history
        if 'history' not in st.session_state:
            st.session_state['history'] = []

        # Initialize messages
        if 'generated' not in st.session_state:
            st.session_state['generated'] = ["Hello ! Ask me about " + uploaded_file.name + " 🤗"]

        if 'past' not in st.session_state:
            st.session_state['past'] = ["Hey ! 👋"]

        # Create containers for chat history and user input
        response_container = st.container()
        container = st.container()

        # User input form
        with container:
            with st.form(key='my_form', clear_on_submit=True):
                user_input = st.text_input("Query:", placeholder="Talk to csv data 👉 (:", key='input')
                submit_button = st.form_submit_button(label='Send')

            if submit_button and user_input:
                output = conversational_chat(user_input)
                st.session_state['past'].append(user_input)
                st.session_state['generated'].append(output)

            # Display chat history
            if st.session_state['generated']:
                with response_container:
                    for i in range(len(st.session_state['generated'])):
                        message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="big-smile")
                        message(st.session_state["generated"][i], key=str(i), avatar_style="thumbs")
