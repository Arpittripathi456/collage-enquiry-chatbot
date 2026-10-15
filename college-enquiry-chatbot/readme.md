# AI-Powered College Enquiry System

A retrieval-based college enquiry chatbot built with Python, Streamlit, pandas, scikit-learn, TF-IDF and cosine similarity.

## Features
- Browser-based question input and answer display
- FAQ retrieval from `faqs.csv`
- Category-labelled answers
- Safe fallback when no sufficiently similar FAQ is found
- CSV dataset that can be edited separately from the application
- Session-based conversation history

## Project files
- `app.py` — Streamlit application
- `faqs.csv` — FAQ dataset with `question`, `answer`, `category` columns
- `requirements.txt` — Python dependencies
- `Test_Cases.csv` — manual test log template
- `Project_Report.pdf` — project report template
- `Project_Presentation.pptx` — presentation

## Requirements
- Python 3.10+ recommended
- pip

## Run locally
1. Open a terminal in the project folder.
2. Create and activate a virtual environment if needed.
3. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
4. Start the application:
   ```bash
   python -m streamlit run app.py
   ```

On Windows, a local launcher may be used if it points to the project's `.venv` Python executable. The launcher is not needed by Streamlit hosting.

## FAQ CSV format
The first row must contain:
```csv
question,answer,category
```
Keep the required column names unchanged. Quote values containing commas. Review duplicate questions and blank answers.

## Retrieval approach
The app vectorizes FAQ questions with TF-IDF and compares a user query using cosine similarity. The highest-scoring FAQ is used only when its score passes the configured threshold. This is lexical retrieval and can misclassify paraphrases; validate with the included test cases.

## Safety and data quality
This prototype is not connected to official college systems. Verify fees, admission dates, eligibility, scholarship rules and placement details against official notices. Do not publish private student information, credentials or secrets. Do not claim tests passed until they have been run and recorded.

## Deployment
Deploy the repository with Streamlit hosting and ensure `app.py`, `faqs.csv`, `requirements.txt` and `README.md` are committed. After each update, verify the hosted app has rebuilt and run representative test questions.
