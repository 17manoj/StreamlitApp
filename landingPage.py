import openai
import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()

# Set your OpenAI API key
openai.api_key = os.getenv("OPEN_API")


# Configurations for Streamlit
st.set_page_config(
    page_title="ChatGPT Q&A with Model Selection",
    page_icon="🔐",
    layout="centered"
)

# Predefined passcode (You can change this to any secure value)
CORRECT_PASSCODE = "1835"

# App Title
st.title("🔐 ChatGPT Q&A with Model Selection")
st.write("A secure Q&A application powered by ChatGPT.")

# Session state for authentication
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Authentication Block
if not st.session_state.authenticated:
    st.subheader("Enter Passcode")
    passcode = st.text_input("Passcode", type="password", placeholder="Enter passcode here...")
    
    if st.button("Submit"):
        if passcode == CORRECT_PASSCODE:
            st.session_state.authenticated = True
            st.success("Access Granted!")
        else:
            st.error("Invalid passcode. Please try again.")
else:
    # If authenticated, show the main Q&A section
    st.subheader("Ask Your Question")

    # Model Selection
    model = st.selectbox(
        "Select the ChatGPT Model:",
        options=["gpt-3.5-turbo", "gpt-4","gpt-4o"],  # Add more models if needed
        help="Choose between GPT-3.5-turbo, GPT-4 and GPT-4o for generating responses."
    )

    # Input Area for the Question
    question = st.text_area("Enter your question:", height=150)

    # Button to Fetch Answer
    if st.button("Get Answer"):
        if question.strip() == "":
            st.warning("Please enter a question!")
        else:
            with st.spinner(f"Fetching response using {model}..."):
                try:
                    # Call OpenAI Chat API
                    response = openai.ChatCompletion.create(
                        model=model,  # Use the selected model
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant."},
                            {"role": "user", "content": question}
                        ],
                        max_tokens=200,
                        temperature=0.7
                    )
                    # Extract and Display the Answer
                    answer = response['choices'][0]['message']['content']
                    st.success("Response:")
                    st.write(answer)
                except Exception as e:
                    st.error(f"An error occurred: {e}")

    # Logout Button
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.warning("You have been logged out.")

# Footer
st.markdown(
    """
    ---
    Built with ❤️ using [Streamlit](https://streamlit.io) and [OpenAI](https://openai.com).
    """
)
