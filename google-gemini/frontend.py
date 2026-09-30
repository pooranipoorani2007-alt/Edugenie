import subprocess
import sys
import time
import os
import requests
import streamlit as st


API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000"
)


# Start FastAPI automatically
@st.cache_resource
def start_backend():

    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "backend:app",
            "--host",
            "127.0.0.1",
            "--port",
            "8000"
        ]
    )

    time.sleep(2)

    return process


backend_process = start_backend()


# -----------------------------
# Configuration
# -----------------------------

API_URL = "http://127.0.0.1:8000"


# -----------------------------
# Streamlit Configuration
# -----------------------------

st.set_page_config(
    page_title="EduGenie",
    page_icon="🎓",
    layout="centered"
)


# -----------------------------
# Header
# -----------------------------

st.title("🎓 EduGenie")
st.subheader("AI-Powered Educational Assistant")

st.write(
    "Learn easily with smart answers, AI-generated quizzes "
    "and personalized learning paths."
)


# -----------------------------
# Scenario 1: Ask Question
# -----------------------------

st.header("📚 Ask a Question")

question = st.text_input(
    "Enter your question:",
    placeholder="Explain photosynthesis in simple words"
)


if st.button("Ask EduGenie"):

    if not question.strip():

        st.warning("Please enter a question.")

    else:

        try:

            with st.spinner("EduGenie is thinking..."):

                response = requests.post(
                    f"{API_URL}/ask",
                    json={
                        "question": question
                    },
                    timeout=60
                )

            if response.status_code == 200:

                data = response.json()

                st.markdown("### 🤖 EduGenie Answer")

                st.markdown(
                    data["answer"]
                )

            elif response.status_code == 429:

                st.error(
                    "Gemini API quota has been exceeded. "
                    "Please try again later."
                )

            else:

                st.error(
                    f"API Error: {response.status_code}"
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "Cannot connect to the EduGenie backend. "
                "Make sure FastAPI is running on port 8000."
            )

        except requests.exceptions.Timeout:

            st.error(
                "The request took too long. Please try again."
            )

        except Exception as e:

            st.error(
                f"Unexpected error: {e}"
            )


# -----------------------------
# Scenario 2: Generate Quiz
# -----------------------------

st.header("📝 Generate Quiz")

topic = st.selectbox(
    "Choose a topic:",
    [
        "Pythagoras Theorem",
        "SQL",
        "Python",
        "Machine Learning"
    ]
)


if st.button("Generate Quiz"):

    try:

        with st.spinner("Generating your quiz..."):

            response = requests.post(
                f"{API_URL}/quiz",
                json={
                    "topic": topic
                },
                timeout=60
            )

        if response.status_code == 200:

            data = response.json()

            st.markdown("### 📝 Your AI-Generated Quiz")

            st.markdown(
                data["quiz"]
            )

        elif response.status_code == 429:

            st.error(
                "Gemini API quota has been exceeded. "
                "Please try again later."
            )

        else:

            st.error(
                f"API Error: {response.status_code}"
            )

    except requests.exceptions.ConnectionError:

        st.error(
            "Cannot connect to the EduGenie backend."
        )

    except requests.exceptions.Timeout:

        st.error(
            "The request took too long. Please try again."
        )

    except Exception as e:

        st.error(
            f"Unexpected error: {e}"
        )


# -----------------------------
# Scenario 3: Learning Path
# -----------------------------

st.header("🛣️ Personalized Learning Path")

learning_topic = st.selectbox(
    "Select learning topic:",
    [
        "SQL",
        "Python",
        "Machine Learning"
    ]
)


if st.button("Create Learning Path"):

    try:

        with st.spinner(
            "Creating your personalized learning path..."
        ):

            response = requests.post(
                f"{API_URL}/learning-path",
                json={
                    "topic": learning_topic
                },
                timeout=60
            )

        if response.status_code == 200:

            data = response.json()

            st.markdown(
                "### 🛣️ Your Personalized Learning Path"
            )

            st.markdown(
                data["learning_path"]
            )

        elif response.status_code == 429:

            st.error(
                "Gemini API quota has been exceeded. "
                "Please try again later."
            )

        else:

            st.error(
                f"API Error: {response.status_code}"
            )

    except requests.exceptions.ConnectionError:

        st.error(
            "Cannot connect to the EduGenie backend."
        )

    except requests.exceptions.Timeout:

        st.error(
            "The request took too long. Please try again."
        )

    except Exception as e:

        st.error(
            f"Unexpected error: {e}"
        )


# -----------------------------
# Footer
# -----------------------------

st.divider()

st.caption(
    "EduGenie – Learn Smart. Learn Simple. 🎓"
)