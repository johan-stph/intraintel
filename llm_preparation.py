import pickle

from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough


template_1 = """Beantworte die Frage mit folgendem Kontext:

Kontext: {context}

Frage: {question}
"""

template_2 = """Use the given context, which is in German, to answer the given question in English. The context is 
given as a list of mediawiki xml articles. Include the following things in your reply: 
1. The answer to the question
2. In which article you found the answer. The name of the article is inside the <title> tag.

Question: {question}

Context: {context}
"""


def create_retriever():
    raw_documents = TextLoader("wiki.xml").load()
    text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=0)
    documents = text_splitter.split_documents(raw_documents)
    db = FAISS.from_documents(documents, OpenAIEmbeddings())
    retriever = db.as_retriever()
    return retriever


# second part

def create_template():
    template = template_2
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
