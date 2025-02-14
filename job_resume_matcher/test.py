import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go

# ...existing code...

def plot_skill_match_score(matched_skills, missing_skills):
    labels = ['Matched Skills', 'Missing Skills']
    values = [matched_skills, missing_skills]

    fig, ax = plt.subplots()
    sns.barplot(x=labels, y=values, ax=ax)
    ax.set_title('Skill Match Score Breakdown')
    ax.set_ylabel('Percentage')
    st.pyplot(fig)

def plot_radar_chart(required_skills, available_skills):
    categories = list(required_skills.keys())
    required_values = list(required_skills.values())
    available_values = list(available_skills.values())

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=required_values,
        theta=categories,
        fill='toself',
        name='Required Skills'
    ))

    fig.add_trace(go.Scatterpolar(
        r=available_values,
        theta=categories,
        fill='toself',
        name='Available Skills'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title='Comparison of Required vs. Available Competencies'
    )

    st.plotly_chart(fig)

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

                    st.write("Extracted Resume Text:")
                    st.write(cleaned_resume_text)
                    st.write("Job Description:")
                    st.write(cleaned_job_description)

                    st.write("Comprehensive Report:")
                    # Match skills and create a comprehensive report
                    report = match_skills(cleaned_resume_text, cleaned_job_description)
                    st.write(report)

                    # Example data for charts
                    matched_skills = 70  # Example percentage of matched skills
                    missing_skills = 30  # Example percentage of missing skills
                    required_skills = {'Skill A': 80, 'Skill B': 90, 'Skill C': 70}  # Example required skills
                    available_skills = {'Skill A': 60, 'Skill B': 85, 'Skill C': 75}  # Example available skills

                    # Plot charts
                    plot_skill_match_score(matched_skills, missing_skills)
                    plot_radar_chart(required_skills, available_skills)
            else:
                st.error("Currently, only PDF files are supported for text extraction.")

if __name__ == "__main__":
    main()