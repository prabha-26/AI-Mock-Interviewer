import os
from groq import Groq
import streamlit as st


def get_groq_client():
    api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not configured. Add it to the Streamlit app secrets."
        )
    return Groq(api_key=api_key)


def generate_question(context, difficulty):

    prompt = f"""
You are an expert technical interviewer.

Based on the following material, generate ONE interview question.

Difficulty level: {difficulty}

Rules:
- Beginner → basic conceptual question
- Intermediate → conceptual + explanation
- Advanced → deeper technical or scenario-based question

Material:
{context}

Return only the question.
"""

    response = get_groq_client().chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    return response.choices[0].message.content.strip()
