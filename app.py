import openai
import streamlit as st
import os

# Fetch API key from Streamlit Secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Streamlit app
st.title("AI-Powered Recommender System")

# Debug: Display the current API key (only first few characters for safety)
st.write(f"Debug: Using API Key: {openai.api_key[:5]}...")

# User input
user_input = st.text_input("Enter your preference (e.g., 'romantic movies', 'laptops'): ")

if user_input:
    try:
        # Try GPT-4 first
        model_name = "gpt-4"
        st.write(f"Debug: Trying model {model_name}")
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant for recommendations."},
                {"role": "user", "content": f"Recommend 5 {user_input}."}
            ]
        )
        recommendations = response['choices'][0]['message']['content']
        st.write("Recommendations:")
        st.write(recommendations)

    except openai.error.OpenAIError as e:
        # Fallback to GPT-3.5 if GPT-4 fails
        st.error(f"GPT-4 Error: {e}. Trying GPT-3.5-turbo as a fallback.")
        try:
            model_name = "gpt-3.5-turbo"
            st.write(f"Debug: Trying model {model_name}")
            response = openai.ChatCompletion.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant for recommendations."},
                    {"role": "user", "content": f"Recommend 5 {user_input}."}
                ]
            )
            recommendations = response['choices'][0]['message']['content']
            st.write("Recommendations:")
            st.write(recommendations)
        except Exception as fallback_error:
            st.error(f"GPT-3.5 Fallback Error: {fallback_error}")


