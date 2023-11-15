import openai
import streamlit as st
openai.api_key = st.secrets["API_KEY"]
st.set_page_config(page_title="Bharat Legal GPT")
file_handler = st.container()
st.title("⚖️ Legal Bharat GPT")
st.write('''Celebrate Legal Empowerment with Bharat Legal GPT: Your Trusted Partner for Instant Legal Clarity and Expert Guidance – Making Law Simple and Accessible for Everyone!''')
st.markdown('\n')
st.markdown('\n')
with file_handler:
    if st.button("🔃 Refresh"):
        st.cache_data.clear()
st.markdown(
    """
    <style>
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob,
    .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137,
    .viewerBadge_text__1JaDK {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Define conversation examples
conversations = [
    {
        "messages": [
            {"role": "system", "content": "Welcome to the Bharat Legal GPT - Your Expert in Indian Legal Matters!"},
            {"role": "user", "content": "What can you do?"},
            {"role": "assistant", "content": "Bharat Legal GPT can assist you with a wide range of Indian legal matters. You can ask me questions about starting a business, patent filing, labor laws, contracts, and more. I can provide information, guidance, and legal insights to help you navigate the complex legal landscape in India. Feel free to ask any legal questions, and I'll do my best to provide you with accurate and helpful answers."},
        ]
    }
]

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
full_response = ""
if prompt := st.chat_input("Enter a prompt here"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    # Append the user's message to the conversation
    conversations[-1]["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        for response in openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=conversations[-1]["messages"],
            stream=True,
        ):
            if response.choices and response.choices[0].delta and response.choices[0].delta.content:
                full_response += response.choices[0].delta.content
                message_placeholder.markdown(full_response + "▌")
            else:
                break  # Exit loop if content is None or not present
        message_placeholder.markdown(full_response)
st.session_state.messages.append({"role": "assistant", "content": full_response})
