import pickle

from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough


def create_retriever():
    raw_documents = TextLoader("hausordnung.txt").load()
    text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=0)
    documents = text_splitter.split_documents(raw_documents)
    db = FAISS.from_documents(documents, OpenAIEmbeddings())
    retriever = db.as_retriever()
    return retriever


# second part

def create_template():
    template = """Übersetzte alle deine Antworten auf Englisch. Beantworte die Frage mit folgendem Kontext:

{context}

Frage: {question}
"""
    prompt = ChatPromptTemplate.from_template(template)
    return prompt


def format_docs(docs):
    return "\n\n".join([d.page_content for d in docs])


def create_chain():
    retriever = create_retriever()
    model = ChatOpenAI()
    prompt = create_template()
    chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | model
            | StrOutputParser()
    )
    return chain
