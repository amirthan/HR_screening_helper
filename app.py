import streamlit as st
import uuid
from langchain.vectorstores import Pinecone
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.schema import Document
import pinecone
from langchain.chains.summarize import load_summarize_chain
from utils import *

# Session variables setup
if 'session_id' not in st.session_state:
    st.session_state['session_id'] =''

def main():
    st.set_page_config(page_title="Resume Analysis Helper")
    st.title("HR - Resume Analysis Helper 🧐")

    with st.sidebar:
        st.subheader("Upload and Input Section")
        job_desc = st.text_area("Insert the 'JOB DESCRIPTION' here...",key="1")
        desired_count = st.slider("Number of 'RESUMES' to return", 1, 50, 10, key="2")
        pdf_files = st.file_uploader("Upload resumes here (PDF format only)", type=["pdf"], accept_multiple_files=True)
        analyze_button = st.button("Analyze Resumes")
        stop_button = st.button("Stop Analysis")
        change_job_desc_button = st.button("Search for new Job Description")  
        pinecone_api_key = st.text_input("Enter your Pinecone API key:", value='', type='password')
        openai_api_key = st.text_input("Enter your OpenAI API key:", value='', type='password')
    
    embeddings_instance = initialize_embeddings() #initialize embeddings instance

    if analyze_button or change_job_desc_button:
        if not pinecone_api_key:
            st.warning("Please enter a valid Pinecone API key.")
            return
        
        with st.spinner('Processing...'):
            if stop_button:  # Check if stop button was pressed
                st.warning("Analysis stopped by user.")
                return
            st.session_state['session_id'] = uuid.uuid4().hex
            if 'uploaded' not in st.session_state:  # Check if resumes have been uploaded already
                document_list = generate_documents(pdf_files, st.session_state['session_id'])
                st.write(f"*Resumes uploaded*: {len(document_list)}")
                
                upload_to_pinecone(pinecone_api_key, "gcp-starter", "resumes", embeddings_instance, document_list)
                st.session_state['uploaded'] = True  # Set uploaded flag in session state
                
                # Check if there are existing resumes in the database
                existing_resumes = check_existing_resumes(pinecone_api_key, "gcp-starter", "resumes", embeddings_instance)
                if existing_resumes:
                    st.write("Matching with existing resumes...")
                    relevant_documents = find_relevant_documents(job_desc, desired_count, pinecone_api_key, "gcp-starter", "resumes", embeddings_instance)
                    display_relevant_documents(relevant_documents, openai_api_key, existing=True)  # Updated to indicate existing resumes
                else:
                    st.warning("No resumes found in the database. Please upload resumes first.")
                    return
                
            else:
                relevant_documents = find_relevant_documents(job_desc, desired_count, pinecone_api_key, "gcp-starter", "resumes", embeddings_instance)
                display_relevant_documents(relevant_documents, openai_api_key)  # Moved to a separate function for reuse
        st.success("Analysis complete. Hope this saves you time! ❤️")
        
    elif change_job_desc_button:  # New code block for change job description button
        if 'uploaded' in st.session_state and st.session_state['uploaded']:
            with st.spinner('Fetching updated results...'):
                embeddings_instance = initialize_embeddings()  # Re-initialize embeddings instance
                relevant_documents = find_relevant_documents(job_desc, desired_count, pinecone_api_key, "gcp-starter", "resumes", embeddings_instance)
                display_relevant_documents(relevant_documents, openai_api_key)  # Reuse function to display results
            st.success("Updated analysis complete. Hope this saves you time! ❤️")
        else:
            st.warning("Please upload resumes and analyze them first.")
            


if __name__ == '__main__':
    main()
