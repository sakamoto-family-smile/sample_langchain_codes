import langchain
from langchain import OpenAI
from langchain.schema import BaseChatMessageHistory, OutputParserException
from langchain.memory import ConversationBufferMemory, RedisChatMessageHistory
from langchain.memory.chat_message_histories import SQLChatMessageHistory
from langchain.agents import initialize_agent, AgentExecutor
from langchain.agents import load_tools
from langchain.cache import RedisCache
import os
import redis


# キャッシュの初期化
CACHE_HOST = str(os.environ.get("LLM_CACHE_HOST"))
CACHE_PORT = int(os.environ.get("LLM_CACHE_PORT"))
CACHE_DB_NUM = 0
redis_for_cache = redis.Redis(host=CACHE_HOST, port=CACHE_PORT, db=CACHE_DB_NUM)
langchain.llm_cache = RedisCache(redis_=redis_for_cache)

# チャットメッセージの保存DBのパラメーター設定
CHAT_DB_HOST = str(os.environ.get("CHAT_DB_HOST"))
CHAT_DB_PORT = int(os.environ.get("CHAT_DB_PORT"))
# CHAT_DB_NUM = 1
CHAT_DB_USER = str(os.environ.get("CHAT_DB_USER"))
CHAT_DB_PASSWORD = str(os.environ.get("CHAT_DB_PASSWORD"))
CHAT_DB_DATABASE_NAME = str(os.environ.get("CHAT_DB_DATABASE_NAME"))


class Agent:
    def __init__(self) -> None:
        self.__memory_key = "chat_history"
        self.__chat_history_id = "chat_history"
        self.__chat_table_name = "message_store"
        self.__agent = self.__get_chat_agent()

    def get_response(self, message: str) -> str:
        try:
            return self.__agent.run(input=message)
        except OutputParserException as e:
            print(e)
            raise AgentException(e)

    def get_chat_history(self) -> dict:
        buffer = self.__agent.memory.load_memory_variables({})
        return buffer[self.__memory_key]

    def __get_chat_agent(self) -> AgentExecutor:
        model_name = "text-davinci-003"
        llm = OpenAI(temperature=0, max_tokens=500, model_name=model_name)
        tool_names = ["google-search", "llm-math", "wikipedia"]
        tools = load_tools(tool_names, llm=llm)  # llm-mathのツールを使うのにLLMが必要
        message_history = self.__get_message_history()
        memory = ConversationBufferMemory(
            memory_key=self.__memory_key, chat_memory=message_history
        )
        agent = initialize_agent(
            tools, llm, agent="zero-shot-react-description", verbose=True, memory=memory
        )
        return agent

    # def __get_message_history_for_redis(self) -> BaseChatMessageHistory:
    #    url = f"redis://{CHAT_DB_HOST}:{CHAT_DB_PORT}/{CHAT_DB_NUM}"
    #    return RedisChatMessageHistory(
    #        session_id=self.__chat_history_id,
    #        url=url,
    #        key_prefix=self.__chat_history_key_prefix,
    #    )

    def __get_message_history(self) -> BaseChatMessageHistory:
        url = f"mysql://{CHAT_DB_USER}:{CHAT_DB_PASSWORD}@{CHAT_DB_HOST}:{CHAT_DB_PORT}/{CHAT_DB_DATABASE_NAME}"
        return SQLChatMessageHistory(
            session_id=self.__chat_history_id,
            connection_string=url,
            table_name=self.__chat_table_name,
        )


class AgentException(Exception):
    pass
