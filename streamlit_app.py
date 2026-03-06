import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

# Page config
st.set_page_config(
    page_title="AI Chat Assistant",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for stunning UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    * {
        font-family: 'Inter', sans-serif;
    }

    /* Main background gradient */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }

    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Header styling */
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem 2rem;
        border-radius: 0 0 30px 30px;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .main-header h1 {
        color: white;
        font-weight: 700;
        font-size: 2.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        margin: 0;
        letter-spacing: 1px;
    }

    .header-icon {
        font-size: 3rem;
        margin-right: 1rem;
        animation: float 3s ease-in-out infinite;
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }

    /* Chat container */
    .chat-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* User message styling */
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 5px 20px;
        margin: 0.5rem 0 0.5rem auto;
        max-width: 75%;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        animation: slideInRight 0.3s ease-out;
    }

    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(30px); }
        to { opacity: 1; transform: translateX(0); }
    }

    /* AI message styling */
    .ai-message {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 20px 5px;
        margin: 0.5rem auto 0.5rem 0;
        max-width: 75%;
        box-shadow: 0 4px 15px rgba(56, 239, 125, 0.3);
        animation: slideInLeft 0.3s ease-out;
    }

    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }

    /* Input styling */
    .stChatInput {
        border-radius: 25px !important;
    }

    div[data-baseweb="input"] {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 25px !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        backdrop-filter: blur(10px);
    }

    div[data-baseweb="input"] input {
        color: white !important;
    }

    div[data-baseweb="input"] input::placeholder {
        color: rgba(255, 255, 255, 0.5) !important;
    }

    /* Button styling */
    .stButton button {
        background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(245, 87, 108, 0.4);
    }

    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(245, 87, 108, 0.6);
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: white !important;
    }

    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown li {
        color: rgba(255, 255, 255, 0.8) !important;
    }

    /* Stats cards */
    .stats-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
    }

    .stats-number {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .stats-label {
        color: rgba(255, 255, 255, 0.7);
        font-size: 0.9rem;
    }

    /* Footer styling */
    .footer {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem 2rem;
        border-radius: 30px 30px 0 0;
        text-align: center;
        margin-top: 2rem;
        box-shadow: 0 -10px 40px rgba(102, 126, 234, 0.3);
    }

    .footer p {
        color: white;
        margin: 0;
        font-size: 0.9rem;
    }

    .footer a {
        color: #38ef7d;
        text-decoration: none;
        font-weight: 600;
    }

    /* Typing indicator */
    .typing-indicator {
        display: flex;
        align-items: center;
        padding: 1rem;
    }

    .typing-dot {
        width: 10px;
        height: 10px;
        background: #38ef7d;
        border-radius: 50%;
        margin: 0 3px;
        animation: typingBounce 1.4s infinite ease-in-out;
    }

    .typing-dot:nth-child(1) { animation-delay: 0s; }
    .typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .typing-dot:nth-child(3) { animation-delay: 0.4s; }

    @keyframes typingBounce {
        0%, 60%, 100% { transform: translateY(0); }
        30% { transform: translateY(-10px); }
    }

    /* Model selector */
    div[data-baseweb="select"] {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }

    div[data-baseweb="select"] > div {
        color: white !important;
    }

    /* Slider styling */
    div[data-baseweb="slider"] {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 0.5rem;
    }

    /* Avatar styling */
    .avatar {
        font-size: 2rem;
        margin-right: 0.5rem;
    }

    .message-wrapper {
        display: flex;
        align-items: flex-start;
        margin: 1rem 0;
    }

    /* Welcome message */
    .welcome-container {
        text-align: center;
        padding: 3rem 1rem;
        animation: fadeIn 0.5s ease-out;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .welcome-icon {
        font-size: 5rem;
        margin-bottom: 1rem;
    }

    .welcome-title {
        font-size: 2rem;
        font-weight: 700;
        color: white;
        margin-bottom: 0.5rem;
    }

    .welcome-subtitle {
        color: rgba(255, 255, 255, 0.7);
        font-size: 1.1rem;
    }

    /* Feature cards */
    .feature-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        transition: all 0.3s ease;
    }

    .feature-card:hover {
        background: rgba(255, 255, 255, 0.1);
        transform: translateY(-3px);
    }

    .feature-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }

    .feature-title {
        color: white;
        font-weight: 600;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize session state variables."""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "total_tokens" not in st.session_state:
        st.session_state.total_tokens = 0


@st.cache_resource
def load_model(model_name, temperature):
    """Load and cache the LLM model."""
    return ChatOllama(model=model_name, temperature=temperature)


@st.cache_resource
def create_chain(model):
    """Create and cache the chain."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful AI assistant."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
    ])
    return prompt | model | StrOutputParser()


def main():
    init_session_state()

    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <h1>⚙️ Settings</h1>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # Model selection
        st.markdown("### 🤖 Model Configuration")
        model_name = st.selectbox(
            "Select Model",
            ["qwen2.5-coder:3b", "llama3.2:3b", "mistral:7b", "codellama:7b"],
            label_visibility="collapsed"
        )

        temperature = st.slider(
            "🌡️ Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Higher values make output more creative"
        )

        max_turns = st.slider(
            "💬 Max Turns",
            min_value=1,
            max_value=20,
            value=5,
            help="Maximum conversation turns"
        )

        st.markdown("---")

        # Stats
        st.markdown("### 📊 Statistics")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"""
            <div class="stats-card">
                <div class="stats-number">{len(st.session_state.messages)}</div>
                <div class="stats-label">Messages</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="stats-card">
                <div class="stats-number">{len(st.session_state.chat_history) // 2}</div>
                <div class="stats-label">Turns</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Clear chat button
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.session_state.messages = []
            st.rerun()

        st.markdown("---")

        # About section
        st.markdown("""
        ### ℹ️ About
        <p style="color: rgba(255,255,255,0.7); font-size: 0.9rem;">
        This AI assistant is powered by LangChain and Ollama.
        It remembers your conversation context for a seamless experience.
        </p>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="margin-top: 1rem;">
            <div class="feature-card">
                <div class="feature-icon">🚀</div>
                <div class="feature-title">Fast Response</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🧠</div>
                <div class="feature-title">Context Aware</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🔒</div>
                <div class="feature-title">Local & Private</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Load model and chain
    llm = load_model(model_name, temperature)
    chain = create_chain(llm)

    # Header
    st.markdown("""
    <div class="main-header">
        <span class="header-icon">✨</span>
        <h1>AI Chat Assistant</h1>
    </div>
    """, unsafe_allow_html=True)

    # Main chat area
    chat_container = st.container()

    with chat_container:
        # Display welcome message if no chat history
        if not st.session_state.messages:
            st.markdown("""
            <div class="welcome-container">
                <div class="welcome-icon">👋</div>
                <div class="welcome-title">Welcome to AI Chat!</div>
                <div class="welcome-subtitle">Start a conversation by typing a message below</div>
            </div>

            <div style="display: flex; justify-content: center; flex-wrap: wrap; margin-top: 2rem;">
                <div class="feature-card" style="width: 150px;">
                    <div class="feature-icon">💬</div>
                    <div class="feature-title">Ask Questions</div>
                </div>
                <div class="feature-card" style="width: 150px;">
                    <div class="feature-icon">💡</div>
                    <div class="feature-title">Get Ideas</div>
                </div>
                <div class="feature-card" style="width: 150px;">
                    <div class="feature-icon">📝</div>
                    <div class="feature-title">Write Code</div>
                </div>
                <div class="feature-card" style="width: 150px;">
                    <div class="feature-icon">🔍</div>
                    <div class="feature-title">Research</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Display chat messages
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="message-wrapper" style="justify-content: flex-end;">
                    <div class="user-message">
                        {message["content"]}
                    </div>
                    <span class="avatar">👤</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="message-wrapper" style="justify-content: flex-start;">
                    <span class="avatar">🤖</span>
                    <div class="ai-message">
                        {message["content"]}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to state
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message
        st.markdown(f"""
        <div class="message-wrapper" style="justify-content: flex-end;">
            <div class="user-message">
                {prompt}
            </div>
            <span class="avatar">👤</span>
        </div>
        """, unsafe_allow_html=True)

        # Get AI response
        with st.spinner(""):
            st.markdown("""
            <div class="message-wrapper" style="justify-content: flex-start;">
                <span class="avatar">🤖</span>
                <div class="ai-message">
                    <div class="typing-indicator">
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            current_turns = len(st.session_state.chat_history) // 2

            if current_turns >= max_turns:
                response = "You've reached the maximum number of turns. Please clear the chat to start a new conversation."
            else:
                response = chain.invoke({
                    "question": prompt,
                    "chat_history": st.session_state.chat_history,
                })

                st.session_state.chat_history.append(HumanMessage(content=prompt))
                st.session_state.chat_history.append(AIMessage(content=response))

                remaining = max_turns - (current_turns + 1)
                if remaining <= 2 and remaining > 0:
                    response += f"\n\n*({remaining} turns remaining)*"

            st.session_state.messages.append({"role": "assistant", "content": response})

            st.rerun()

    # Footer
    st.markdown("""
    <div class="footer">
        <p>Made with 💜 by <strong>AI Chat Assistant</strong> | Powered by
        <a href="https://langchain.com" target="_blank">LangChain</a> &
        <a href="https://ollama.ai" target="_blank">Ollama</a>
        </p>
        <p style="font-size: 0.8rem; margin-top: 0.5rem; opacity: 0.8;">
            Your conversations are private and run locally on your machine.
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()