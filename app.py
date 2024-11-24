import openai
import streamlit as st
import csv
import os

# Fetch the API key securely
# If running locally, use environment variables or a .env file.
# If deployed on Streamlit Cloud, use secrets manager.
openai.api_key = os.getenv("OPENAI_API_KEY", st.secrets.get("OPENAI_API_KEY"))

# Ensure the feedback file exists
if not os.path.exists("feedback.csv"):
    with open("feedback.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["User Input", "Recommendations", "Feedback"])

# Streamlit app title
st.title("AI-Powered Recommender System")

# Get user input
user_input = st.text_input("Enter your preference (e.g., 'romantic movies', 'laptops'): ")

if user_input:
    # Call OpenAI API to generate recommendations
    with st.spinner("Generating recommendations..."):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful recommender system."},
                    {"role": "user", "content": f"Recommend 5 {user_input}."}
                ],
                temperature=0.7,
            )
            recommendations = response['choices'][0]['message']['content']
        except Exception as e:
            st.error(f"Error: {e}")
            recommendations = None

    # Display recommendations if successful
    if recommendations:
        st.write("Recommendations:")
        st.write(recommendations)

        # Collect feedback
        feedback = st.slider("Rate these recommendations (1-5):", 1, 5)
        if st.button("Submit Feedback"):
            with open("feedback.csv", "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([user_input, recommendations, feedback])
            st.success("Thank you for your feedback!")

# Optional: Show feedback data for debugging
if st.checkbox("Show feedback data (for debugging)"):
    if os.path.exists("feedback.csv"):
        with open("feedback.csv", "r") as f:
            st.text(f.read())
    else:
        st.warning("No feedback data available yet.")

