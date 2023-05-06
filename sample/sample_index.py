from langchain.document_loaders import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper

import os


def main(doc_path: str, question: str):
    loader = PyPDFLoader(file_path=doc_path)
    index: VectorStoreIndexWrapper = VectorstoreIndexCreator().from_loaders([loader])

    # 質問する
    answer = index.query(question=question)
    print(answer)


if __name__ == "__main__":
    print("---- start main ----")
    # doc_path = os.path.join(os.path.dirname(__file__), "data", "2305.00944.pdf")
    # question = "tell me the abstract of this document."
    doc_path = os.path.join(os.path.dirname(__file__), "data", "jle0000901210.pdf")
    question = "この文章の要約を教えてください。"
    main(doc_path=doc_path, question=question)
    print("---- end main ----")
