from langchain.llms import OpenAI


def main():
    llm = OpenAI(temperature=0.7)
    text = "カラフルな靴下を作る会社の社名として、何かいいものはないですか？日本語の社名でお願いします。"
    prediction = llm(text)
    print(prediction.strip())


if __name__ == "__main__":
    print("---- start main ----")
    main()
    print("---- end main ----")
