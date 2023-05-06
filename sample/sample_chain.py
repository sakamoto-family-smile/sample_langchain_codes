from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


def main(baseball_player_in_major_league: str):
    llm = OpenAI(temperature=0)
    prompt = PromptTemplate(
        input_variables=["player"],
        template="2023年の{player}のメジャーリーグにおけるホームラン数を教えてください。",
    )
    chain = LLMChain(llm=llm, prompt=prompt)

    answer = chain.run(baseball_player_in_major_league)
    print(answer)


if __name__ == "__main__":
    print("---- start main ----")
    player_name = "大谷翔平"
    main(baseball_player_in_major_league=player_name)
    print("---- end main ----")
