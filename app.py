import streamlit as st
import google.generativeai as genai
import os
from datetime import datetime

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="AI Productivity Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS FOR PROFESSIONAL LOOK
# ============================================================
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .main-header h1 { color: white; margin: 0; font-size: 2.3rem; }
    .main-header p { color: rgba(255,255,255,0.9); margin-top: 0.5rem; }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white; border: none; border-radius: 8px;
        padding: 0.5rem 1.5rem; font-weight: 600;
        transition: transform 0.2s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px; padding: 0 20px;
        background-color: #f0f2f6;
        border-radius: 8px; font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    .disclaimer {
        background: #fff3cd; border-left: 4px solid #ffc107;
        padding: 1rem; border-radius: 8px; margin: 1rem 0;
    }
    .output-box {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# API CONFIGURATION
# ============================================================
def get_api_key():
    try:
        return st.secrets["GEMINI_API_KEY"]
    except (KeyError, FileNotFoundError):
        return os.environ.get("GEMINI_API_KEY", "")

API_KEY = get_api_key()

if not API_KEY:
    st.error("⚠️ **API Key Not Found.**")
    st.info("Add your Gemini API key to `.streamlit/secrets.toml` (local) or to Streamlit Cloud secrets (deployed). Get a free key at https://aistudio.google.com/")
    st.stop()

genai.configure(api_key=API_KEY)

@st.cache_resource
def get_model():
    return genai.GenerativeModel("gemini-2.0-flash")

model = get_model()

# ============================================================
# HELPER FUNCTIONS
# ============================================================
def generate_response(prompt, temperature=0.7):
    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(temperature=temperature)
        )
        return response.text, None
    except Exception as e:
        return None, str(e)

def show_disclaimer():
    st.markdown("""
    <div class="disclaimer">
        <strong>⚠️ Responsible AI Notice:</strong> AI-generated content may contain errors or bias.
        Always review, verify facts, and check for confidentiality before professional use.
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.title("🤖 AI Assistant")
    st.markdown("---")

    st.subheader("⚙️ Settings")
    temperature = st.slider(
        "Creativity Level", 0.0, 1.0, 0.7, 0.1,
        help="Lower = focused & factual. Higher = creative."
    )

    st.markdown("---")
    st.subheader("📊 Session Stats")

    for key in ["email_count", "summary_count", "plan_count", "research_count", "chat_count"]:
        if key not in st.session_state:
            st.session_state[key] = 0

    st.metric("📧 Emails", st.session_state.email_count)
    st.metric("📝 Summaries", st.session_state.summary_count)
    st.metric("📅 Plans", st.session_state.plan_count)
    st.metric("🔍 Research", st.session_state.research_count)
    st.metric("💬 Chats", st.session_state.chat_count)

    st.markdown("---")
    st.caption("Built with Streamlit + Google Gemini")
    st.caption("© 2025 AI Skill Accelerator")

# ============================================================
# MAIN HEADER
# ============================================================
st.markdown("""
<div class="main-header">
    <h1>🤖 AI Productivity Assistant</h1>
    <p>Your all-in-one workplace assistant — automate emails, meetings, planning, research, and more</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# TABS
# ============================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "✉️ Email Generator",
    "📝 Notes Summarizer",
    "📅 Task Planner",
    "🔍 Research Assistant",
    "💬 AI Chatbot"
])

# ============================================================
# TAB 1: SMART EMAIL GENERATOR
# ============================================================
with tab1:
    st.header("✉️ Smart Email Generator")
    st.write("Generate context-aware professional emails with the right tone for any audience.")

    col1, col2 = st.columns(2)
    with col1:
        recipient = st.selectbox("Recipient", ["Client", "Manager", "Team Member", "Colleague", "Vendor", "Other"])
        tone = st.selectbox("Tone", ["Formal", "Informal", "Persuasive", "Friendly", "Urgent", "Apologetic"])
    with col2:
        purpose = st.text_input("Purpose", placeholder="e.g., Request a project update")
        length = st.selectbox("Length", ["Short (under 100 words)", "Medium (100-200 words)", "Detailed (200+ words)"])

    key_points = st.text_area(
        "Key points to include (one per line):",
        placeholder="Deadline extended to Friday\nNeed feedback by Wednesday\nAttached: Q4 report",
        height=100
    )

    if st.button("🚀 Generate Email", key="email_btn", use_container_width=True):
        if not purpose:
            st.warning("Please enter the purpose of the email.")
        else:
            with st.spinner("✍️ Crafting your email..."):
                prompt = f"""You are a professional business communication expert.
Write a {tone.lower()} email to a {recipient.lower()} regarding: {purpose}.
Email length: {length}.
Key points to include:
{key_points}

Requirements:
- Use an appropriate subject line at the top (format: Subject: ...)
- Keep it concise, clear, and professional
- Structure with greeting, body, and sign-off
- Sign off with "Best regards" and a placeholder [Your Name]
"""
                result, error = generate_response(prompt, temperature)
                if error:
                    st.error(f"Error: {error}")
                else:
                    st.session_state.email_count += 1
                    st.subheader("📧 Generated Email")
                    st.markdown(f'<div class="output-box">{result}</div>', unsafe_allow_html=True)
                    st.download_button(
                        "📥 Download Email",
                        data=result,
                        file_name=f"email_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                        mime="text/plain"
                    )
    show_disclaimer()

# ============================================================
# TAB 2: MEETING NOTES SUMMARIZER
# ============================================================
with tab2:
    st.header("📝 Meeting Notes Summarizer")
    st.write("Transform lengthy meeting notes into a concise, structured summary with action items.")

    notes = st.text_area(
        "Paste your meeting notes or transcript here:",
        height=250,
        placeholder="Paste raw notes, minutes, or transcript..."
    )

    col1, col2 = st.columns(2)
    with col1:
        summary_style = st.selectbox("Summary Style", ["Executive Summary", "Bullet Points", "Detailed Breakdown"])
    with col2:
        include_actions = st.checkbox("Include Action Items Table", value=True)

    if st.button("🚀 Summarize Notes", key="notes_btn", use_container_width=True):
        if not notes:
            st.warning("Please paste some meeting notes first.")
        else:
            with st.spinner("🧠 Analyzing and summarizing..."):
                action_instruction = (
                    "Include a clear Markdown table with columns: Action Item | Owner | Deadline."
                    if include_actions else "List action items as bullet points."
                )
                prompt = f"""You are an expert executive assistant.
Summarize the following meeting notes using this style: {summary_style}.

Extract and clearly highlight:
1. **Key Decisions Made**
2. **Action Items** (with responsible person and deadline if mentioned)
3. **Key Discussion Points**
4. **Overall 3-sentence Summary**

{action_instruction}

Use clean Markdown formatting with headings.
Only extract information explicitly stated — do not invent facts.

Meeting Notes:
{notes}
"""
                result, error = generate_response(prompt, temperature)
                if error:
                    st.error(f"Error: {error}")
                else:
                    st.session_state.summary_count += 1
                    st.subheader("📋 Meeting Summary")
                    st.markdown(result)
                    st.download_button(
                        "📥 Download Summary",
                        data=result,
                        file_name=f"meeting_summary_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                        mime="text/markdown"
                    )
    show_disclaimer()

# ============================================================
# TAB 3: AI TASK PLANNER
# ============================================================
with tab3:
    st.header("📅 AI Task Planner / Scheduler")
    st.write("Generate an optimized schedule that prioritizes tasks by urgency and importance.")

    col1, col2 = st.columns(2)
    with col1:
        timeframe = st.selectbox("Plan For", ["Today", "Tomorrow", "This Week"])
        work_hours = st.selectbox("Working Hours", ["08:00 - 17:00", "09:00 - 18:00", "07:00 - 16:00", "10:00 - 19:00"])
    with col2:
        energy_peak = st.selectbox("Peak Energy Time", ["Morning", "Afternoon", "Evening"])

    tasks = st.text_area(
        "List your tasks (one per line, add deadlines in brackets if any):",
        height=180,
        placeholder="Finish project report [today 5pm]\nReply to client emails\nPrepare slides for tomorrow\nUpdate team on progress\nReview budget proposal [Friday]"
    )

    if st.button("🚀 Generate Plan", key="planner_btn", use_container_width=True):
        if not tasks:
            st.warning("Please enter your tasks.")
        else:
            with st.spinner("🗓️ Building your optimized plan..."):
                prompt = f"""You are a certified productivity coach using the Eisenhower Matrix.

Create a structured {timeframe.lower()} plan.
Working hours: {work_hours}. Peak energy: {energy_peak}.

Tasks:
{tasks}

Deliverables:
1. **Priority Matrix Table** with columns: Task | Urgent? | Important? | Quadrant | Priority (High/Med/Low)
2. **Hourly Timeline** from start to end of working day, with buffer times between tasks.
3. **3 Time Optimization Strategies** tailored to these specific tasks.
4. **Top 3 Focus Tasks** for the day.

Use Markdown tables and headings for clean formatting.
"""
                result, error = generate_response(prompt, temperature)
                if error:
                    st.error(f"Error: {error}")
                else:
                    st.session_state.plan_count += 1
                    st.subheader("📅 Your Optimized Plan")
                    st.markdown(result)
                    st.download_button(
                        "📥 Download Plan",
                        data=result,
                        file_name=f"plan_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                        mime="text/markdown"
                    )
    show_disclaimer()

# ============================================================
# TAB 4: AI RESEARCH ASSISTANT
# ============================================================
with tab4:
    st.header("🔍 AI Research Assistant")
    st.write("Get structured insights and recommendations on any topic or article.")

    col1, col2 = st.columns(2)
    with col1:
        research_type = st.selectbox("Research Type", ["Topic Overview", "Article Summary", "Deep Analysis", "Pros & Cons"])
    with col2:
        audience = st.selectbox("Audience Level", ["General", "Professional", "Academic", "Beginner"])

    research_input = st.text_area(
        "Enter a topic, paste an article, or describe what you want researched:",
        height=200,
        placeholder="e.g., 'The impact of AI on small businesses in South Africa' or paste a full article..."
    )

    if st.button("🚀 Research", key="research_btn", use_container_width=True):
        if not research_input:
            st.warning("Please enter a topic or article.")
        else:
            with st.spinner("🔎 Researching..."):
                prompt = f"""You are a senior research analyst.
Research Type: {research_type}.
Audience: {audience}.

Content to analyze:
{research_input}

Provide:
1. **Executive Summary** (3-4 sentences)
2. **Key Insights** (5 bullets)
3. **Supporting Details** (organized by theme)
4. **Recommendations** (3-5 actionable points)
5. **Further Questions** to explore

Format using clean Markdown. If it's a topic, provide a balanced, factual overview.
Do not fabricate sources or statistics.
"""
                result, error = generate_response(prompt, temperature)
                if error:
                    st.error(f"Error: {error}")
                else:
                    st.session_state.research_count += 1
                    st.subheader("📚 Research Report")
                    st.markdown(result)
                    st.download_button(
                        "📥 Download Report",
                        data=result,
                        file_name=f"research_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                        mime="text/markdown"
                    )
    show_disclaimer()

# ============================================================
# TAB 5: AI CHATBOT
# ============================================================
with tab5:
    st.header("💬 AI Workplace Chatbot")
    st.write("Ask anything about productivity, workplace tasks, or general assistance.")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "👋 Hi! I'm your AI workplace assistant. Ask me anything — productivity tips, email phrasing, task prioritization, or general workplace help."}
        ]

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    if user_input := st.chat_input("Type your message here..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Build conversation context
                context = "\n".join(
                    f"{m['role'].capitalize()}: {m['content']}"
                    for m in st.session_state.messages[-6:]
                )
                prompt = f"""You are a helpful, professional workplace AI assistant.
Respond concisely and practically. Offer examples when useful.
Do not invent facts. If unsure, say so.

Conversation so far:
{context}

Assistant:"""
                result, error = generate_response(prompt, temperature)
                if error:
                    st.error(f"Error: {error}")
                else:
                    st.session_state.chat_count += 1
                    st.markdown(result)
                    st.session_state.messages.append({"role": "assistant", "content": result})

    if st.button("🗑️ Clear Chat", key="clear_chat"):
        st.session_state.messages = [
            {"role": "assistant", "content": "👋 Chat cleared. How can I help you?"}
        ]
        st.rerun()

    show_disclaimer()

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.caption("🤖 AI Productivity Assistant • Built for the AI Skill Accelerator Programme • Powered by Google Gemini & Streamlit")
