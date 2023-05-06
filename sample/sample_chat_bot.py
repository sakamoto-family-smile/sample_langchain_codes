import langchain
from langchain import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentExecutor
from langchain.agents import load_tools

# キャッシュを設定
# from langchain.cache import InMemoryCache
# langchain.llm_cache = InMemoryCache()

# from langchain.cache import SQLiteCache
# langchain.llm_cache = SQLiteCache(database_path=".langchain.db")

from langchain.cache import RedisCache
import redis

redis = redis.Redis(host="localhost", port=6379, db=0)
langchain.llm_cache = RedisCache(redis_=redis)


def get_chat_agent() -> AgentExecutor:
    model_name = "text-davinci-003"  # "text-davinci-003", "gpt-3.5-turbo"
    llm = OpenAI(temperature=0, max_tokens=500, model_name=model_name)
    # tool_names = ["serpapi", "llm-math", "wikipedia"]
    tool_names = ["google-search", "llm-math", "wikipedia"]
    tools = load_tools(tool_names, llm=llm)  # llm-mathのツールを使うのにLLMが必要
    memory = ConversationBufferMemory(memory_key="chat_history")
    agent = initialize_agent(
        tools, llm, agent="zero-shot-react-description", verbose=True, memory=memory
    )
    return agent


def main_loop(agent: AgentExecutor):
    print("----- prompt template -----")
    print(agent.agent.llm_chain.prompt.template)
    print("---------------------------")
    user_input = input("You: ")

    while True:
        response = agent.run(input=user_input)
        print(f"AI: {response}")
        user_input = input("You: ")
        if user_input == "exit":
            break

    # 登録されたredisのキーをprint表示する
    # r = redis.Redis(host="localhost", port=6379, db=0)
    # for key in r.scan_iter("*"):
    #    print(key)


if __name__ == "__main__":
    print("---- start main ----")
    agent = get_chat_agent()
    main_loop(agent=agent)
    print("---- end main ----")
