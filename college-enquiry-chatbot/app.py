import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="College Enquiry Chatbot",
    page_icon="🎓"
)

st.title("🎓 College Enquiry Chatbot")
st.write("Welcome to BIT Raipur College Enquiry System!")

question = st.text_input("Ask your question:")

BASE_DIR = os.path.dirname(os.path.abspath(_file_))
faqs = pd.read_csv(os.path.join(BASE_DIR, "faqs.csv"))

answers = {
    "courses": "BIT Raipur offers engineering courses, including CSE.",
    "fees": "Please contact the college office for the latest fee details.",
    "admission": "Please contact the college office for admission details.",
    "hostel": "Please contact the college office for hostel fees and facilities.",
    "placements": "Please contact the college for placement details.",
    "timing": "Please contact the college office for class timings.",
    "contact": "Please check the official BIT Raipur website for contact details."
}

if st.button("Ask"):
    if question.strip():
        found = False

        for keyword, answer in answers.items():
            if keyword in question.lower().strip():
                st.success(answer)
                found = True
                break

        if not found:
            st.info("Sorry, please contact the college office for this information.")
    else:
        st.warning("Please enter a question first.")
