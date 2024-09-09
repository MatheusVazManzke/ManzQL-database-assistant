from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.core.tools import QueryEngineTool
from llama_index.core.objects import (
    SQLTableNodeMapping,
    ObjectIndex,
    SQLTableSchema,
)

from llama_index.core.indices.struct_store.sql_query import (
    SQLTableRetrieverQueryEngine,
)
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import StorageContext, load_index_from_storage

class SQLQueryEngine:
    def __init__(self, sql_database, tables):
        self.tool = QueryEngineTool.from_defaults(
            query_engine=NLSQLTableQueryEngine(sql_database=sql_database, tables=tables),
            name="query_engine",
            description="A SQL query engine that allows you to interact with a connected MySQL database"
        )
    
class LocalDatabaseInfo:
    def __init__(self, sql_database, tables):
        self.sql_database = sql_database
        self.table_node_mapping = SQLTableNodeMapping(sql_database)
        self.table_schema_objs = [SQLTableSchema(table_name=table) for table in tables]

        self.obj_index = ObjectIndex.from_objects(
            self.table_schema_objs,
            self.table_node_mapping,
            VectorStoreIndex,
        )
        self.table_query_engine = SQLTableRetrieverQueryEngine(
            sql_database, self.obj_index.as_retriever(similarity_top_k=1)
        )
        self.tool = QueryEngineTool.from_defaults(
            query_engine=self.table_query_engine,
            name="tables_and_schemas",
            description="It gives you all the information on the database's tables and their schemas."
        )

class SQLProfessor:
    def __init__(self, storage_context):
        self.index = load_index_from_storage(storage_context)
        self.index_tool = QueryEngineTool.from_defaults(
            query_engine=self.index.as_query_engine(),
            name="SQL_professor",
            description="A SQL engine that you can use to write better and more complex MySQL queries. You can use it if the database is not recognizing your SQL queries as valid."
        )
