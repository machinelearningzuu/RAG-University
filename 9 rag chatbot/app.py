import streamlit as st
from PyPDF2 import PdfReader
import yaml, os, openai, textwrap
from langchain.chains import LLMChain
from langchain.vectorstores import FAISS
from langchain.vectorstores import Chroma
from InstructorEmbedding import INSTRUCTOR
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.memory import ConversationBufferMemory
from langchain.document_loaders import DirectoryLoader
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.schema.messages import HumanMessage, SystemMessage
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from html_template import css, bot_template, user_template

with open('cadentials.yaml') as f:
    credentials = yaml.load(f, Loader=yaml.FullLoader)

os.environ['OPENAI_API_KEY'] = credentials['OPENAI_API_KEY']
os.environ['HUGGINGFACEHUB_API_TOKEN'] = credentials['HUGGINGFACEHUB_API_TOKEN']
os.environ['ENGINE'] = credentials['ENGINE']

openai.api_key = credentials['OPENAI_API_KEY']
openai.api_base = credentials['OPENAI_API_BASE']
openai.api_type = credentials['OPENAI_API_TYPE']
openai.api_version = credentials['OPENAI_API_VERSION']
openai.engine = credentials['ENGINE']

bge_embeddings = HuggingFaceBgeEmbeddings(
                                        model_name="BAAI/bge-base-en",
                                        model_kwargs={'device': 'mps'},
                                        encode_kwargs={'normalize_embeddings': True} # set True to compute cosine similarity
                                        )


openai_llm = ChatOpenAI(
                        openai_api_key=os.environ["OPENAI_API_KEY"],
                        engine = os.environ["ENGINE"],
                        model='gpt-3.5-turbo',
                        temperature=0.9, 
                        max_tokens = 256,
                        )

system_template = """You have to act like My girl friend, who named "bubu". Use the following pieces of context to answer the users question. 
    ----------------
    {context}"""

    # Create the chat prompt templates
messages = [
            SystemMessagePromptTemplate.from_template(system_template),
            HumanMessagePromptTemplate.from_template("{question}")
            ]
qa_prompt = ChatPromptTemplate.from_messages(messages)

def get_pdf_text(docs):
    text = ""

    for pdf in docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()

    return text

def get_text_chunks(text):
    text_spitter = CharacterTextSplitter(
                                        separator="\n",
                                        chunk_size = 100,
                                        chunk_overlap = 50,
                                        length_function = len
                                        )

    chunks = text_spitter.split_text(text)
    return chunks

def get_vectors(text_chunks):
    vectorstore = FAISS.from_texts(
                                texts = text_chunks, 
                                embedding = bge_embeddings
                                )
    return vectorstore

def get_conversation_chain(vectorstore):
    memory = ConversationBufferMemory(
                                    memory_key='chat_history', 
                                    return_messages=True
                                    )
    conversation_chain = ConversationalRetrievalChain.from_llm(
                                                            llm=openai_llm,
                                                            retriever=vectorstore.as_retriever(
                                                                                            search_type="mmr", 
                                                                                            search_kwargs={
                                                                                                            'k': 5, 
                                                                                                            'lambda_mult': 0.25
                                                                                                            }),
                                                            memory=memory,
                                                            combine_docs_chain_kwargs={"prompt": qa_prompt}
                                                            )
    return conversation_chain

def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
            
def main():
    # st.set_page_config(page_title='Scaled RAG for Production', page_icon='🔗', layout='wide')

    # st.header('Scaled RAG Pipeline for Production')
    # st.text_input("Ask your question here : ")

    # with st.sidebar:
    #     st.subheader("Your Documents")
    #     st.file_uploader(
    #                     "Upload your documents here", 
    #                     type=['pdf', 'txt'],
    #                     accept_multiple_files=True
    #                     )
    #     st.button("Process")
    #     # if st.button("Process"):
    #     #     with st.spinner("Processing"):
    #             # get PDF texts 

    #             # get the text chunks 

    #             # create vector store

    st.set_page_config(page_title='Talk with Bubu ❤️', page_icon='🔗', layout='wide')
    st.write(css, unsafe_allow_html=True)
    

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None


    st.header("Talk with Bubu ❤️")
    user_question = st.text_input("Ask your question here : ")
    #static_prompt = 'Help me to get answers from this unstructured data, question: '
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Documents")
        documents = st.file_uploader(
            "Upload your PDFs here, click 'Process'", accept_multiple_files=True)
        
        
        if st.button("Process"):
            with st.spinner("Processing"):
                print(documents)
                raw_text = get_pdf_text(documents)

                chunk_text = get_text_chunks(raw_text)

                vector_store = get_vectors(chunk_text)

                st.session_state.conversation  = get_conversation_chain(vector_store)
           

if __name__ == '__main__':
    main()