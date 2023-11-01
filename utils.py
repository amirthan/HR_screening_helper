
import openai
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.llms import OpenAI
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.schema import Document
import pinecone
from pypdf import PdfReader
from langchain.llms.openai import OpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.llms import HuggingFaceHub
import streamlit as st


def extract_text_from_pdf(pdf_file):
    content = ""
    pdf_reader = PdfReader(pdf_file)
    for page in pdf_reader.pages:
        content += page.extract_text()
    return content

def generate_documents(uploaded_pdfs, session_id):
    documents = []
    for file in uploaded_pdfs:
        text_content = extract_text_from_pdf(file)
        documents.append(Document(
            page_content=text_content,
            metadata={"name": file.name,"type=":file.type,"size":file.size,"session_id":session_id},
        ))
    return documents

def initialize_embeddings():
    return SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

def upload_to_pinecone(api_key, environment, index_name, embeddings_instance, document_list):
    pinecone.init(api_key=api_key, environment=environment)
    Pinecone.from_documents(document_list, embeddings_instance, index_name=index_name)
    
#TODO add a function to wait and confirm that the index is ready before proceeding after the uploading 
# need to check that the pdfs content or the metadata is already there.

def download_from_pinecone(api_key, environment, index_name, embeddings_instance):
    pinecone.init(api_key=api_key, environment=environment)
    return Pinecone.from_existing_index(index_name, embeddings_instance)

def find_relevant_documents(user_query, num_docs, api_key, environment, index_name, embeddings_instance):
    index = download_from_pinecone(api_key, environment, index_name, embeddings_instance)
    return index.similarity_search_with_score(user_query, int(num_docs))

def summarize_document(document,openai_api_key):
    st.write("Summarizing document...")
    language_model = OpenAI(temperature=0, openai_api_key=openai_api_key)
    summarization_chain = load_summarize_chain(language_model, chain_type="map_reduce")
    return summarization_chain.run([document])

            
# function to handle existing resumes
def check_existing_resumes(pinecone_api_key, environment, index_name, embeddings_instance):
    pinecone.init(api_key=pinecone_api_key, environment=environment)
    #index = Pinecone.from_existing_index(index_name, embeddings_instance)
    return pinecone.describe_index("resumes").metadata_config is not None

# display relevant documents with existing flag
def display_relevant_documents(relevant_documents, openai_api_key, existing=False): 
    st.write(":heavy_minus_sign:" * 30)
    for idx, doc in enumerate(relevant_documents):
        st.subheader(f"👉 {idx + 1}")
        st.write(f"**File**: {doc[0].metadata['name']}")
        if existing:
            st.write(f"(From existing resumes)")
        with st.expander('Details 👀'):
            st.info(f"**Match Score**: {doc[1]}")
            st.write(f"***{doc[0].page_content}")
            doc_summary = summarize_document(doc[0],openai_api_key)
            st.write("this is the doc summary")
            st.write(f"**Summary**: {doc_summary}")