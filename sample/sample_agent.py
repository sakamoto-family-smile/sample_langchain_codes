from tabnanny import verbose
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.llms import OpenAI


def main(question: str):
    llm = OpenAI(temperature=0.7)
    tools = load_tools(
        ["serpapi", "llm-math", "wikipedia"], llm=llm
    )  # llm-mathのツールを使うのにLLMが必要
    agent = initialize_agent(
        tools, llm, agent="zero-shot-react-description", verbose=True
    )
    answer = agent.run((question))
    print("--- prompt template ---")
    print(agent.agent.llm_chain.prompt.template)
    print("----------")
    print("--- answer ---")
    print(answer)
    print("----------")


if __name__ == "__main__":
    print("---- start main ----")
    # question = "2023年5月1日の東京の最高気温は何度でしたか？摂氏温度でお答え下さい。また、その数値を x としたとき、x^0.23 は何ですか？"
    question = "メジャーリーガーである大谷翔平のホームラン数を教えてください。期間を、2023年4月1日から2023年4月30日までとします。"
    # question = "漫画である「HUNTER X HUNTER」の概要を教えてください。"
    main(question=question)
    print("---- end main ----")
