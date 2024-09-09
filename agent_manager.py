from llama_index.core.agent import ReActAgent
from llama_tools import SQLQueryEngine, LocalDatabaseInfo
from llama_index.llms.ollama import Ollama

class AgentManager:
    def __init__(self, db, tables, verbose=True):
        """
        Initializes the AgentManager with the provided tools.
        
        :param tools: A list of tools to be used by the agent.
        :param verbose: A flag to set the verbosity of the agent.
        """
        self.sql_query_tool = SQLQueryEngine(db, tables)
        self.database_info_tool = LocalDatabaseInfo(db, tables)
        self.verbose = verbose
        self.agent = None
    
    def initialize_agent(self):
        """
        Initializes the ReActAgent with the provided tools.
        :return: None
        """
        self.agent = ReActAgent.from_tools(tools=[self.sql_query_tool.tool, self.database_info_tool.tool], verbose=self.verbose, llm=Ollama(model="codeqwen", request_timeout=120.0))
        print("Agent initialized successfully!")

    def get_agent(self):
        """
        Returns the initialized agent.
        :return: The ReActAgent object.
        """
        if self.agent is None:
            raise RuntimeError("Agent has not been initialized. Call initialize_agent() first.")
        return self.agent

    def reset_agent(self):
        """
        Resets the agent to allow re-initialization.
        :return: None
        """
        self.agent = None
        print("Agent has been reset.")
