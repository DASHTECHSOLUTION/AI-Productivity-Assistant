import streamlit as st
import google.generativeai as genai

# Configure the Gemini API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Set up the page
st.set_page_config(page_title="AI Productivity Assistant", page_icon="🤖", layout="wide")
st.title("🤖 AI Productivity Assistant")
st.write("Your all-in-one workplace assistant. Select a tool below to get started.")

# Create the three tabs
tab1, tab2, tab3 = st.tabs(["✉️ Smart Email Generator", "📝 Meeting Notes Summarizer", "📅 AI Task Planner"])

# --- TAB 1: SMART EMAIL GENERATOR ---
with tab1:
    st.header("Smart Email Generator")
    st.write("Generate professional emails with the right tone and audience.")
    
    col1, col2 = st.columns(2)
    with col1:
        recipient = st.selectbox("Recipient:", ["Client", "Manager", "Team Member", "Colleague", "Other"])
        tone = st.selectbox("Tone:", ["Formal", "Informal", "Persuasive", "Friendly", "Urgent"])
    with col2:
        purpose = st.text_input("Purpose of email:", placeholder="e.g., Request a meeting, Apologize for delay")
        key_points = st.text_area("Key points to include (one per line):", placeholder="New deadline is Friday\nNeed feedback by Wednesday")

    if st.button("Generate Email", key="email_btn"):
        if not purpose:
            st.warning("Please enter the purpose of the email.")
        else:
            with st.spinner("Generating your email..."):
                prompt = f"""You are a professional email assistant. 
Write a {tone.lower()} email to a {recipient.lower()} regarding: {purpose}.
Include these key points: {key_points}.
Keep the email concise, clear, and professional. 
Sign off with 'Best regards' and leave a placeholder for the sender's name."""
                
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(prompt)
                st.subheader("📧 Your Generated Email")
                st.write(response.text)

# --- TAB 2: MEETING NOTES SUMMARIZER ---
with tab2:
    st.header("Meeting Notes Summarizer")
    st.write("Convert lengthy notes into concise summaries with action items.")
    
    notes = st.text_area("Paste your meeting notes here:", height=250, placeholder="Paste the full transcript or notes here...")

    if st.button("Summarize Notes", key="notes_btn"):
        if not notes:
            st.warning("Please paste some meeting notes first.")
        else:
            with st.spinner("Summarizing your notes..."):
                prompt = f"""You are an expert executive assistant. 
Summarize the following meeting notes into a concise format.
Extract and clearly highlight:
1. Key Decisions Made
2. Action Items (with the responsible person and deadline)
3. General Key Points
4. Overall 3-sentence Summary

Format the output using Markdown with clear headings and bullet points.
Meeting Notes: {notes}"""
                
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(prompt)
                st.subheader("📝 Meeting Summary")
                st.markdown(response.text)

# --- TAB 3: AI TASK PLANNER ---
with tab3:
    st.header("AI Task Planner / Scheduler")
    st.write("Generate a structured schedule and prioritize your tasks.")
    
    tasks = st.text_area("List your tasks (one per line):", placeholder="Finish project report\nReply to client emails\nPrepare slides for tomorrow\nUpdate team on progress")
    timeframe = st.selectbox("Plan for:", ["Today", "Tomorrow", "This Week"])
    
    if st.button("Generate Plan", key="planner_btn"):
        if not tasks:
            st.warning("Please enter your tasks.")
        else:
            with st.spinner("Creating your optimized plan..."):
                prompt = f"""You are a productivity coach and expert scheduler.
Create a structured {timeframe.lower()} plan based on the following tasks:
{tasks}

Instructions:
1. Prioritize the tasks using the Eisenhower Matrix (Urgent vs. Important).
2. Create a timeline from 8:00 AM to 5:00 PM, including buffer times.
3. Suggest 3 specific time optimization strategies for these tasks.

Format the output in Markdown with a clear table or timeline structure."""
                
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(prompt)
                st.subheader("📅 Your Optimized Plan")
                st.markdown(response.text)
