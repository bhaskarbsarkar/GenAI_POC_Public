import streamlit as st
from agent.linkedin_crew import LinkedinCrew  # Assuming Agent is defined in agent/__init__.py
import os
from utils import read_file
import time 

st.set_page_config(page_title="LinkedIn Copywriter", layout="wide")

def main():
    st.title("CrewAI LinkedIn Copywriter")
    
    post_type = st.selectbox(
        "Select the type of post you want to create:",
        ["Normal Post", "Tool Demo Post"]
    )

    user_input = st.text_area("Enter your content to design the LinkedIn Post:")
    uploaded_files = st.file_uploader("Upload your text files or documents", type=["txt", "pdf"], accept_multiple_files=True)
    
    if st.button("Submit"):
        content = user_input
        
        if uploaded_files:
            for uploaded_file in uploaded_files:
                file_content = read_file(uploaded_file)
                if file_content == "":
                    st.warning(f"Please upload valid text files or documents. Skipping {uploaded_file}")
                else:
                    content += "\n" + file_content
                    st.success(f"Successfully uploaded {uploaded_file}")
        
        if content.strip():
            with st.status("Processing...", expanded=True) as status:
                crew = LinkedinCrew()
                
                st.write("Generating Post...")
                if post_type == "Tool Demo Post":
                    post_response = crew.generate_tool_demo_post(content)
                else:
                    post_response = crew.generate_normal_post(content)
                    # post_response = "Post"
                status.update(label="Post Generated!", state="complete")
                time.sleep(2)
                status.update(label="Generating Hooks...", state="running")

                st.write("Generating Hooks...")
                hooks_response = crew.generate_hooks(content)
                # hooks_response = "Hooks"
                status.update(label="Hooks Generated!", state="complete")
                time.sleep(2)
                status.update(label="Generating Comments...", state="running")
                st.write("Generating Comments...")
                comments_response = crew.generate_comments(content)
                # comments_response = "Comments"
                status.update(label="Comments Generated!", state="complete")
                time.sleep(2)
                status.update(label="Done!", state="complete")   

            col1, col2 = st.columns([2, 1])    
            with col1:
                    st.header("Generated Post\n---")
                    st.markdown(post_response)
                    
                    st.header("Generated Comments")
                    st.markdown(comments_response)
                
            with col2:
                st.header("Generated Hooks")
                st.markdown(hooks_response)
        else:
            st.warning("Please enter your content or upload files.")

if __name__ == "__main__":
    main()