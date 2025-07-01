# 📁 File: app.py

import streamlit as st
from chatbot import answer_question
from admin_upload import handle_admin_upload
from feedback import save_feedback
import datetime
import os

st.set_page_config(page_title="Nutrition & Meal Planner Chatbot", layout="wide")

st.title("🥦 Nutrition & Meal Planner Chatbot")

st.write("""
Welcome! I'm your nutrition assistant for children.  
Choose options below and ask your own questions!
""")

# -- Dropdown Inputs
age = st.selectbox("Select Child's Age", options=[str(i) for i in range(1, 18)])
diet_type = st.selectbox("Diet Type", options=["Vegetarian", "Non-Vegetarian", "Eggetarian"])

# -- Chat Input
user_query = st.text_input("Enter your question:")

# -- Ask Question
if st.button("Ask"):
    if not user_query.strip():
        st.warning("Please enter your question.")
    else:
        with st.spinner("Generating response..."):
            response = answer_question(user_query)
            
            # Extract and clean response text (assumes you already changed answer_question to return result text)
            # Limit to first 6 lines to keep it short & neat
            # lines = response.split("\n")
            # short_response = "\n".join(lines[:10])
            # if len(lines) > 10:
            #     short_response += "\n\n*...more details available on request*"

            # Display using markdown for better formatting
            st.markdown(response)
        # with st.spinner("Thinking..."):
        #     full_query = f"My child is {age} years old and follows a {diet_type} diet. {user_query}"
        #     response = answer_question(full_query)
        #     st.success(response)

            # Save chat history
            with open("chat_history.txt", "a", encoding="utf-8") as f:
                f.write(f"[{datetime.datetime.now()}]\nQ: {user_query}\nA: {response}\n\n")

# -- Feedback Form
st.markdown("---")
st.subheader("💬 Leave Feedback")
feedback = st.text_area("Your feedback")
if st.button("Submit Feedback"):
    save_feedback(feedback)
    st.success("Thanks for your feedback!")

# -- Admin Upload Section
st.markdown("---")
st.subheader("🔐 Admin Upload")
handle_admin_upload()