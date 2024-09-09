This is a personal project—

ManzQL is a database assistant that runs locally using pre-trained models via Ollama (currently hardcoded to use 'codeqwen' for all its functions). It has two main functions: helping me write SQL queries (using RAG on text-to-SQL datasets) and directly interacting with a database of my choice. 
As I write this, I’m reading relevant LLM papers and using this code to test the agentic capabilities various open-source models and different approaches to RAG (Retrieval-Augmented Generation).

The user interface is done with Streamlit. It allows me to connect to any database of my choice.
![Alt Text](https://github.com/MatheusVazManzke/ManzQL-database-assistant/blob/main/images/example1.png)

Using natural language, I can ask the agent to query my database. In the example bellow, I have uploaded the classic titanic dataset to a local mysql database.
![Alt Text](https://github.com/MatheusVazManzke/ManzQL-database-assistant/blob/main/images/example1.png)
