import os
import re
import pandas as pd
import streamlit as st

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="College Enquiry Chatbot",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 College Enquiry Chatbot")
st.write("Welcome to BIT Raipur College Enquiry System!")

st.caption(
    "Ask questions about courses, admission, fees, "
    "hostel, scholarships and placements."
)


# --------------------------------------------------
# 2. FAQ DATASET
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "faqs.csv")


def normalize_text(text):
    """Normalize text for question matching."""
    text = str(text).lower().strip()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


@st.cache_data
def load_faqs(file_path):

    if not os.path.isfile(file_path):
        raise FileNotFoundError(
            "faqs.csv file nahi mili. "
            "Use app.py ke same folder mein rakho."
        )

    df = pd.read_csv(file_path, encoding="utf-8-sig")
    df.columns = df.columns.str.strip().str.lower()

    required_columns = {"question", "answer", "category"}

    if not required_columns.issubset(df.columns):
        raise ValueError(
            "faqs.csv mein question, answer aur category "
            "columns hone chahiye."
        )

    df = df[["question", "answer", "category"]].copy()

    for column in ["question", "answer", "category"]:
        df[column] = df[column].fillna("").astype(str).str.strip()

    df = df[
        (df["question"] != "") &
        (df["answer"] != "")
    ].reset_index(drop=True)

    if df.empty:
        raise ValueError(
            "faqs.csv mein valid questions aur answers nahi hain."
        )

    df["normalized_question"] = df["question"].apply(normalize_text)

    return df


# --------------------------------------------------
# 3. LOAD FAQ DATA
# --------------------------------------------------

try:
    faqs = load_faqs(CSV_PATH)

except (FileNotFoundError, ValueError, pd.errors.ParserError) as error:
    st.error(f"FAQ Dataset Error: {error}")
    st.stop()


# --------------------------------------------------
# 4. TF-IDF MODEL
# --------------------------------------------------

try:
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        stop_words="english"
    )

    faq_matrix = vectorizer.fit_transform(
        faqs["question"].tolist()
    )

except ValueError:
    st.error(
        "FAQ questions se matching model nahi ban paaya. "
        "faqs.csv ke questions check karo."
    )
    st.stop()


# --------------------------------------------------
# 5. CHAT HISTORY
# --------------------------------------------------

if "history" not in st.session_state:
    st.session_state.history = []


for item in st.session_state.history:
    with st.chat_message("user"):
        st.write(item["question"])

    with st.chat_message("assistant"):
        st.markdown(item["answer"])


# --------------------------------------------------
# 6. QUESTION INPUT
# --------------------------------------------------

question = st.chat_input(
    "Ask about courses, admission, fees or hostel..."
)


# --------------------------------------------------
# 7. QUESTION MATCHING
# --------------------------------------------------

if question and question.strip():

    clean_question = question.strip()
    normalized_question = normalize_text(clean_question)

    answer = None

    # First: exact match
    exact_matches = faqs[
        faqs["normalized_question"] == normalized_question
    ]

    if not exact_matches.empty:

        matched_row = exact_matches.iloc[0]

        answer = (
            f"**Category:** {matched_row['category']}\n\n"
            f"{matched_row['answer']}"
        )

    else:

        # Second: TF-IDF and cosine similarity
        query_vector = vectorizer.transform([clean_question])

        scores = cosine_similarity(
            query_vector,
            faq_matrix
        )[0]

        best_index = int(scores.argmax())
        best_score = float(scores[best_index])

        # Conservative threshold for unrelated questions
        if best_score >= 0.25:

            matched_row = faqs.iloc[best_index]

            answer = (
                f"**Category:** {matched_row['category']}\n\n"
                f"{matched_row['answer']}"
            )

        else:

            answer = (
                "I could not find a sufficiently similar verified "
                "answer in my FAQ dataset. Please contact the "
                "college office for reliable information."
            )

    # Save question and answer
    st.session_state.history.append({
        "question": clean_question,
        "answer": answer
    })

    st.rerun()


# --------------------------------------------------
# 8. FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Information is based on the available FAQ dataset. "
    "Please verify important details with official college "
    "notices or the college office."
)
    
