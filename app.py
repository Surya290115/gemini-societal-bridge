import streamlit as st
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

# 1. Enforce a predictable schema configuration for the AI output
class EmergencyActionPlan(BaseModel):
    severity_level: str = Field(description="Critical, High, Medium, or Low")
    key_extracted_facts: list[str] = Field(description="List of verified facts extracted from the input data")
    immediate_actions: list[str] = Field(description="Step-by-step critical procedures to execute instantly")

# 2. Build a quick visual dashboard setup
st.set_page_config(page_title="Gemini Societal Bridge", layout="centered")
st.title("🌍 Gemini Societal Benefit Bridge")
st.subheader("Transforming messy real-world clutter into life-saving actions")

# User configuration input area
input_type = st.selectbox("Select Input Data Type", ["Frantic Audio Transcript", "Messy Field Notes", "Unorganized Medical History"])
raw_text = st.text_area("Paste the messy, unorganized raw logs here:", height=150)
api_key = st.text_input("Enter your Gemini API Key:", type="password")

if st.button("Generate Action Plan Pipeline"):
    if not api_key:
        st.warning("Please enter your Gemini API key to proceed.")
    elif not raw_text:
        st.warning("Please add some text data to parse.")
    else:
        with st.spinner("Processing input through Gemini engine..."):
            try:
                # Initialize the Google GenAI SDK client
                client = genai.Client(api_key=api_key)
                
                prompt = f"Analyze this unstructured {input_type}. Filter noise and extract critical data:\n{raw_text}"
                
                # Request structured JSON format from the model
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=EmergencyActionPlan,
                        temperature=0.1
                    ),
                )
                
                st.success("Parsing Complete!")
                st.write(response.text)
            except Exception as e:
                st.error(f"An execution error occurred: {e}")
