import streamlit as st
from modules.utils import ask_gemini
from modules.dynamic_kb import has_knowledge_base_changed
from modules.rag import create_vector_db
from modules.multimodal import analyze_image
from modules.medical_chat import ask_medical_bot
from modules.arxiv_chat import ask_arxiv_bot

st.set_page_config(page_title="AI Assistant", page_icon="🤖")

# SIDEBAR
st.sidebar.title("Control Panel")

mode = st.sidebar.radio(
    "Choose Assistant",
    ["Customer Service", "Medical Q&A", "Research Expert"]
)

# Dynamic Header
if mode == "Customer Service":
    st.title("🤖 Customer Service Assistant")
elif mode == "Medical Q&A":
    st.title("🩺 Medical Expert Assistant")
else:
    st.title("📚 Research Expert Assistant")

st.sidebar.markdown("---")
st.sidebar.write("### Available Modes")
st.sidebar.write("🤖 Customer Service")
st.sidebar.write("🩺 Medical Q&A")
st.sidebar.write("📚 Research Expert")


# SESSION STATE

if "customer_messages" not in st.session_state:
    st.session_state.customer_messages = []

if "medical_messages" not in st.session_state:
    st.session_state.medical_messages = []

if "research_messages" not in st.session_state:
    st.session_state.research_messages = []

if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0

st.sidebar.markdown("---")

# Clear chats
if st.sidebar.button("🗑 Clear Customer Chat"):
    st.session_state.customer_messages = []
    st.rerun()

if st.sidebar.button("🩺 Clear Medical Chat"):
    st.session_state.medical_messages = []
    st.rerun()

if st.sidebar.button("📚 Clear Research Chat"):
    st.session_state.research_messages = []
    st.rerun()


# CURRENT CHAT HISTORY

if mode == "Customer Service":
    current_messages = st.session_state.customer_messages
elif mode == "Medical Q&A":
    current_messages = st.session_state.medical_messages
else:
    current_messages = st.session_state.research_messages

# Display history
for msg in current_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# FILE UPLOADER (Customer Only)

uploaded_file = None
if mode == "Customer Service":
    uploaded_file = st.file_uploader(
        "Upload screenshot (optional)",
        type=["png", "jpg", "jpeg"],
        key=f"uploader_{st.session_state.uploader_key}"
    )

prompt = st.chat_input("Ask something...")


# DYNAMIC KB UPDATE

if mode == "Customer Service":
    if has_knowledge_base_changed():
        with st.spinner("Updating knowledge base..."):
            create_vector_db()


# MAIN CHAT LOGIC

if prompt:
    current_messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    answer = ""
    sentiment = ""


    # CUSTOMER SERVICE MODE

    if mode == "Customer Service":
        image_context = ""

        if uploaded_file is not None:
            with st.spinner("Analyzing screenshot..."):
                try:
                    image_context = analyze_image(uploaded_file)
                except Exception as e:
                    st.warning("Image analysis unavailable right now. Continuing with text only.")
                    print(e)
                    image_context = ""

        if image_context:
            enhanced_prompt = f"""
                You are a technical support assistant.

                Use the screenshot analysis as primary evidence.
                Do NOT give generic customer-service answers.
                Reason step-by-step about the technical issue.

                USER QUESTION:
                {prompt}

                IMAGE ANALYSIS:
                {image_context}

                FINAL ANSWER:
            """
            try:
                answer, sentiment = ask_gemini(
                    enhanced_prompt,
                    original_query=prompt,
                    force_no_rag=True
                )
            except Exception as e:
                answer = "Customer service model is busy right now. Please try again."
                sentiment = "ERROR"
                print(e)
        else:
            try:
                answer, sentiment = ask_gemini(prompt)
            except Exception as e:
                answer = "Customer service model is busy right now. Please try again."
                sentiment = "ERROR"
                print(e)


    # MEDICAL MODE

    elif mode == "Medical Q&A":
        with st.spinner("Searching medical knowledge base..."):
            try:
                answer = ask_medical_bot(prompt)
                sentiment = "MEDICAL"
            except Exception as e:
                answer = "Medical model is busy right now. Please try again."
                sentiment = "ERROR"
                print(e)


    # RESEARCH MODE

    else:
        with st.spinner("Searching research papers..."):
            try:
                answer = ask_arxiv_bot(prompt)
                sentiment = "RESEARCH"
            except Exception as e:
                answer = "Research model is busy right now. Please try again."
                sentiment = "ERROR"
                print(e)

    current_messages.append({
        "role": "assistant",
        "content": answer
    })

    with st.chat_message("assistant"):
        st.markdown(answer)

    # Reset uploader after image usage
    if uploaded_file is not None:
        st.session_state.uploader_key += 1
        st.rerun()