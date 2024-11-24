import openai
import streamlit as st

# Fetch the API key from Streamlit Secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Streamlit app logic
st.title("AI-Powered Recommender System")

user_input = st.text_input("Enter your preference (e.g., 'romantic movies', 'laptops'): ")

if user_input:
    try:
        # Generate recommendations
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful recommender system."},
                {"role": "user", "content": f"Recommend 5 {user_input}."}
            ]
        )
        recommendations = response['choices'][0]['message']['content']
        st.write("Recommendations:")
        st.write(recommendations)
    except Exception as e:
        st.error(f"Error: {e}")

