from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough

raw_documents = TextLoader("hausordnung.txt").load()
text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=0)
documents = text_splitter.split_documents(raw_documents)
db = FAISS.from_documents(documents, OpenAIEmbeddings())
retriever = db.as_retriever()

# second part

template = """Beantworte die Frage mit folgendem Kontext:

{context}

Frage: {question}
"""
prompt = ChatPromptTemplate.from_template(template)
model = ChatOpenAI()


def format_docs(docs):
    return "\n\n".join([d.page_content for d in docs])


chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
)

output = chain.invoke("Was gilt es beim Internet zu beachten?")
print(output)
