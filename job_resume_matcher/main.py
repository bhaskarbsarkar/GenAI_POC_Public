import os
from dotenv import load_dotenv
load_dotenv()
USER_AGENT = os.getenv("USER_AGENT")

import streamlit as st
import fitz  # PyMuPDF
from langchain_community.document_loaders import WebBaseLoader
# from transformers import pipeline
from langchain_google_genai import  ChatGoogleGenerativeAI
import nltk
from nltk.corpus import stopwords
import re
from langchain_core.prompts import ChatPromptTemplate

# Download NLTK data
# nltk.download('stopwords')
# stop_words = set(stopwords.words('english'))

# Set the USER_AGENT environment variable
# os.environ["USER_AGENT"] = "your_user_agent_string"

# Set the page configuration
st.set_page_config(page_title="Resume Job Matcher")

# Initialize the ChatGoogleGenerativeAI instance once
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=1,
)

def read_prompt_from_file(file_path):
    with open(file_path, "r") as file:
        return file.read() 

def ask_llm(prompt):
    response = llm.invoke(prompt)
    if response and hasattr(response, 'content'):
        response = response.content  # Extract the content from the BaseMessage
    else:
        response = "No response from the model."
    return response


def extract_text_from_pdf(pdf_file):
    document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text += page.get_text()
    return text

def fetch_job_description(url):
    # scrapingant_loader = ScrapingAntLoader(
    #     [url],  # List of URLs to scrape
    #     api_key=os.getenv("SCRAPY_API_KEY"),  # Get your API key from https://scrapingant.com/
    #     continue_on_failure=False,  # Ignore unprocessable web pages and log their exceptions
    # )
    # loader = scrapingant_loader.load()

    try:
        loader = WebBaseLoader(web_path=url)
        content = loader.load()[0].page_content
    except Exception as e:
        st.error(f"Failed to fetch job description: {e}")
        content = ""
    return content

    # return " ".join(loader)

def clean_text(text, type):
    clean_text_sys_prompt = read_prompt_from_file("job_resume_matcher/resources/prompts/clean_text_system_promp.txt")

    prompt_template = ChatPromptTemplate([
        ("system", clean_text_sys_prompt),
        ("human", "I am providing you {type}. Based upon the instructions, provide me the extracted info in plain text without PREAMBLE and text formatting. Find the content below from which you have to extract the details. \n\n{text}")
    ])

    prompt = prompt_template.invoke({
        "type": type,
        "text": text
    })

    response_text = ask_llm(prompt)

    # # Remove special characters and numbers
    # text = re.sub(r'[^a-zA-Z\s]', '', response_text)
    # # Convert text to lowercase
    # text = text.lower()
    # # Remove stop words
    # global stop_words
    # text = ' '.join([word for word in text.split() if word not in stop_words])
    return response_text


def match_skills(resume_text, job_description):

    system_prompt = read_prompt_from_file("job_resume_matcher/resources/prompts/match_skills_system_prompt.txt")

    human_prompt = read_prompt_from_file("job_resume_matcher/resources/prompts/match_skills_human_prompt.txt")

    prompt_template = ChatPromptTemplate([("system", system_prompt),
                                          ("human", human_prompt)])
    
    prompt = prompt_template.invoke({
        "resume_text": resume_text,
        "job_description": job_description
    })  # Generate the prompt

    response = ask_llm(prompt)

    return response


def main():
    st.title("Job Resume Matcher")

    st.header("Upload Your Resume")
    resume_file = st.file_uploader("Choose a file", type=["pdf"])

    st.header("Enter Job Description Link")
    job_description_link = st.text_input("Job Description URL")

    if st.button("Submit"):
        if resume_file is None:
            st.error("Please upload a resume.")
        elif not job_description_link:
            st.error("Please enter a job description link.")
        else:
            if resume_file.type == "application/pdf":
                with st.spinner("Processing..."):
                    resume_text = extract_text_from_pdf(resume_file)
                    job_description = fetch_job_description(job_description_link)
                    st.success("Resume and Job Description Link -- Submitted successfully!")
                    
                    # Clean the extracted text
                    if resume_text != "" and job_description != "":
                        st.success("Resume and Job Description Details -- Extracted successfully!")
                    else:
                        st.error("Failed to extract resume and job description details.")
                    
                    cleaned_resume_text = clean_text(resume_text, "resume")
                    cleaned_job_description = clean_text(job_description, "job_desc")

                    # st.write("Extracted Resume Text:")
                    # st.write(cleaned_resume_text)
                    # st.write("Job Description:")
                    # st.write(cleaned_job_description)

                    st.header("Comprehensive Report:", divider="blue")
                    # Match skills and create a comprehensive report
                    report = match_skills(cleaned_resume_text, cleaned_job_description)
                    st.write(report)
            else:
                st.error("Currently, only PDF files are supported for text extraction.")

if __name__ == "__main__":
    main()