import streamlit as st
from db_connection import DatabaseConnector
from agent_manager import AgentManager
from llama_index.core import Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


Settings.llm = Ollama(model="codeqwen", request_timeout=120.0)
Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)

# Initialize the db_connector in session state if it doesn't already exist
if 'db_connector' not in st.session_state:
    st.session_state.db_connector = DatabaseConnector() 


# Streamlit interface
st.title("ManzQL - Your database assistant by ManzkeLabs")

# User inputs for database connection details
st.sidebar.header("Database Connection Details")
db_type = st.sidebar.selectbox("Select Database Type", ["mysql", "postgresql", "sqlite"])
user = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")
host = st.sidebar.text_input("Host", value="localhost")
port = st.sidebar.number_input("Port", min_value=1, max_value=65535, value=3306)
db_name = st.sidebar.text_input("Database Name")

# Button to connect to the database
if st.sidebar.button("Connect to Database"):
    try:
        st.session_state.db_connector.create_engine(db_type, user, password, host, port, db_name)
        st.session_state.db_connector.connect_to_db()
        st.success(f"Connected to {db_name} successfully!")
    except Exception as e:
        st.error(f"Failed to connect to the database: {str(e)}")

# Button to close the connection
if st.sidebar.button("Close Connection"):
    try:
        st.session_state.db_connector.close_connection()
        st.success("Connection closed successfully!")
    except Exception as e:
        st.error(f"Failed to close the connection: {str(e)}")

# # Example operation: Show available tables
# if db_connector.sql_database:
#     st.write("Connected to the following tables:")
#     st.write(db_connector.sql_database.get_table_names())

# Sidebar for Agent Initialization
st.sidebar.header("ReAct Agent Initialization")
if st.sidebar.button("Initialize Agent"):
    try:
        # Initialize the agent and store it in session state
        st.session_state.agent = AgentManager(st.session_state.db_connector.sql_database, ['titanic'])
        st.session_state.agent.initialize_agent()

        st.success("Agent initialized successfully!")
    except Exception as e:
        st.error(f"Failed to initialize agent: {str(e)}")

# Check if the agent has been initialized
if 'agent' in st.session_state:
    st.write("Agent is ready for queries.")
else:
    st.write("Please initialize the agent first.")
    
# Chat Interface
if "messages" not in st.session_state: # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question your database"}
    ]
    
if "chat_engine" not in st.session_state: # Initialize the chat engine
    st.session_state.chat_engine = st.session_state.agent.agent

if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.query(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message) # Add response to message history