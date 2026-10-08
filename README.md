# AI Productivity Assistant

## Project Overview
This project is a multi-tool AI Productivity Assistant built for the AI Skill Accelerator Programme. It solves real-world workplace problems by automating repetitive tasks using Google's Gemini AI. The application features three core tools accessible via a single, tabbed interface.

## Features

### 1. Smart Email Generator ✉️
- **Context-Based Generation:** Adapts emails to your specific purpose.
- **Tone Variations:** Supports Formal, Informal, Persuasive, Friendly, and Urgent tones.
- **Audience Adaptation:** Tailors language for Clients, Managers, and Team Members.

### 2. Meeting Notes Summarizer 📝
- **Concise Summarization:** Distills long transcripts into executive summaries.
- **Key Extraction:** Identifies key points, decisions made, and action items.
- **Accountability Tracking:** Highlights deadlines and assigns responsibilities to specific people.

### 3. AI Task Planner / Scheduler 📅
- **Structured Planning:** Creates daily or weekly schedules.
- **Priority Matrix:** Prioritizes tasks based on urgency and importance (Eisenhower Matrix).
- **Time Optimization:** Suggests strategies to batch tasks and improve efficiency.

## Tools Used
- **Streamlit:** Python framework for building the multi-tab web interface.
- **Google Gemini API:** Free AI model (gemini-1.5-flash) for all text generation.
- **GitHub:** Repository hosting and documentation.

## Sample Prompts Used
1. **Email:** "Write a {tone} email to a {recipient} regarding: {purpose}. Include these key points: {key_points}."
2. **Notes:** "Summarize the following notes. Extract key decisions, action items (with owners and deadlines), and a 3-sentence summary."
3. **Planner:** "Create a {timeframe} plan for these tasks: {tasks}. Prioritize using the Eisenhower Matrix and suggest 3 time optimization strategies."

## Responsible AI Considerations
- **Human-in-the-Loop:** All AI-generated content (emails, summaries, schedules) must be reviewed by a human before sending or acting upon.
- **Data Privacy:** Users are advised not to paste confidential company information into the app.
- **Bias Awareness:** AI may generate biased language; prompts are designed to be neutral, and users are encouraged to check for inclusivity.
- **Validation Checks:** Users should verify all dates, names, and deadlines extracted by the summarizer.

## Challenges and Solutions
| Challenge | Solution |
|---|---|
| Managing multiple features in one app | Used Streamlit's `st.tabs()` function to keep the UI clean and organized. |
| AI hallucinating deadlines | Instructed the AI to only extract what is explicitly stated in the notes. |
| API key security | Used Streamlit secrets and `.gitignore` to avoid exposing the key on GitHub. |
| Emails sounding robotic | Added specific tone and audience parameters to the prompt. |

## How to Run Locally
1. Clone this repository:
   ```bash
   git clone https://github.com/DASHTECHSOLUTION/AI-Productivity-Assistant.git
   cd AI-Productivity-Assistant
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   streamlit run app.py
   ```

## How to Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub account
3. Select the `DASHTECHSOLUTION/AI-Productivity-Assistant` repository
4. Add your `GEMINI_API_KEY` in the advanced settings
5. Deploy and share the live URL with your lecturer

## Author
Mahlori Makwakwa
