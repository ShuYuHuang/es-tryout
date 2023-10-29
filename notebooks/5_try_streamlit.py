## Prerequisits:
# pip install streamlit
# pip install streamlit-chat  # For chat interface components
# pip install langchain

# For Streamlit
import streamlit as st
from streamlit_chat import message

# For tackling uploaded files
import tempfile
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter

# For searching form base
from langchain.vectorstores.elasticsearch import ElasticsearchStore
from langchain.embeddings.openai import OpenAIEmbeddings

import dotenv
dotenv.load_dotenv()
ES_URL = "http://localhost:9200"

embeddings_fn = OpenAIEmbeddings(request_timeout=60)
text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0) # can be pre-loaded

# Function to store file in Elasticsearch
@st.cache_resource()
def store_file_in_elasticsearch(uploaded_file, index_name="paragraph-index"):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as tmp_file:
            # Save a temporary file
            file_contents = uploaded_file.getvalue()
            
            tmp_file.write(file_contents)
            tmp_file_path = tmp_file.name
    # Load data
    loader = TextLoader(tmp_file_path) # csv as example, but will include more
    # Chunk data
    
    docs = loader.load_and_split(text_splitter)
    # Store them to ElasticSearch DB
    return ElasticsearchStore.from_documents(
        docs, 
        embeddings_fn, 
        es_url=ES_URL, 
        index_name=index_name,
        distance_strategy="COSINE"
        # distance_strategy="EUCLIDEAN_DISTANCE"
        # distance_strategy="DOT_PRODUCT"
    )

if __name__ == '__main__':

    # Setup openai replyer
    llm = ChatOpenAI(
        model_name='gpt-3.5-turbo',
        temperature=0,
        max_tokens = 256
    )
    template ="""
Queried results form database:
```
{queried}
```

History:
```
{history}
```

You are asked:
{input}

The questions are all related to either query results or history

If the question is related to querying results:
- Extract information from queried result and answer the question
Else if the question is related to history:
- Extract information from history and answer the question
If the question is not related to either querying result or history:
- Politely inform that the result is not related to either history or database
    """

    prompt = PromptTemplate(
        template=template,
        input_variables=["history", "input", "queried"]
    )
    conversation = LLMChain(
        llm=llm,
        verbose=True,
        prompt=prompt,
    )
    

    # Set the title for the Streamlit app
    st.title("Chat TXT - 🦜🦙")

    # Create a file uploader in the sidebar
    uploaded_file = st.sidebar.file_uploader("Upload File", type="txt")
    
  

    # Handle file upload
    if uploaded_file:
        
        db = store_file_in_elasticsearch(uploaded_file, index_name="paragraph-index")
        # Initialize chat history
        if 'history' not in st.session_state:
            st.session_state['history'] = []

        # Function for conversational chat
        def conversational_chat(query):
            db.client.indices.refresh(index="paragraph-index")
            queried_docs = db.similarity_search(query, k=5)
            result = conversation.predict(
                input=user_input,
                history="\n".join(map(lambda x: f"user:{x[0]} | robot:{x[1]}",st.session_state['history'])),
                queried = "\n".join(map(lambda x: x.page_content, queried_docs))
            )
            st.session_state['history'].append((query, result))
            return result

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
                user_input = st.text_input("Query:", placeholder="Talk to txt data 👉 (:", key='input')
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
