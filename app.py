import openai
import streamlit as st

# Fetch API key from Streamlit secrets
api_key = st.secrets.get("OPENAI_API_KEY", None)
if not api_key:
    st.error("No API key found in Streamlit secrets!")
else:
    st.write(f"Debug: Using API Key: {api_key[:5]}...")

openai.api_key = api_key

# User input
st.title("AI-Powered Recommender System")
user_input = st.text_input("Enter your preference (e.g., 'romantic movies', 'laptops'): ")

if user_input:
    try:
        # Debugging: Show which model is being used
        model_name = "gpt-4"
        st.write(f"Debug: Trying model {model_name}")

        response = openai.ChatCompletion.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Recommend 5 {user_input}."}
            ]
        )
        recommendations = response['choices'][0]['message']['content']
        st.write("Recommendations:")
        st.write(recommendations)

    except openai.error.InvalidRequestError as e:
        st.error(f"Invalid request: {e}")
        if "gpt-4" in str(e).lower():
            st.error("You might not have access to GPT-4. Switching to GPT-3.5-turbo.")
            try:
                # Fallback to GPT-3.5
                model_name = "gpt-3.5-turbo"
                response = openai.ChatCompletion.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": f"Recommend 5 {user_input}."}
                    ]
                )
                recommendations = response['choices'][0]['message']['content']
                st.write("Recommendations:")
                st.write(recommendations)
            except Exception as fallback_error:
                st.error(f"GPT-3.5-turbo Error: {fallback_error}")
    except Exception as e:
        st.error(f"Unexpected Error: {e}")





