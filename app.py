import openai
import streamlit as st

# Fetch the OpenAI API key from Streamlit Secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Streamlit app setup
st.title("AI-Powered Recommender System")
st.write("Enter your preferences and get personalized recommendations.")

# Debugging: Show partial API key for verification (optional)
st.write(f"Debug: Using API Key: {openai.api_key[:5]}...")

# User input
user_input = st.text_input("Enter your preference (e.g., 'romantic movies', 'laptops'): ")

if user_input:
    try:
        # Attempt to use GPT-4 for recommendations
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
        if "quota" in str(e).lower():
            # Handle quota exceeded error
            st.error("Error: Your OpenAI API quota has been exceeded. Please check your plan or wait for the quota to reset.")
        elif "model" in str(e).lower():
            # Handle model access issue
            st.error(f"Error: The model '{model_name}' is unavailable or you do not have access to it. Switching to GPT-3.5-turbo.")
            try:
                # Fallback to GPT-3.5-turbo
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
        else:
            # Handle any other errors
            st.error(f"Unexpected Error: {e}")




