import streamlit as st
import os
import openai
openai.api_key = st.secrets["API_KEY"]
st.set_page_config(page_title="Bharat Legal GPT")
file_handler = st.container()
st.title("⚖️ Bharat Legal GPT")
st.write('''Celebrate Legal Empowerment with Bharat Legal GPT: Your Trusted Partner for Instant Legal Clarity and Expert Guidance – Making Law Simple and Accessible for Everyone!''')
st.markdown('\n')
st.markdown('\n')
with file_handler:
    if st.button("🔃 Refresh"):
        st.cache_data.clear()
hide_github_icon = """
#MainMenu {
  visibility: hidden;
}
"""
st.markdown(hide_github_icon, unsafe_allow_html=True)
# Define conversation examples
conversations = [
    {
        "messages": [
            {"role": "system", "content": "Welcome to the Bharat Legal GPT - Your Expert in Indian Legal Matters!"},
            {"role": "user", "content": "What are the legal requirements for starting a new business in India?"},
            {"role": "assistant", "content": "To start a new business in India, you typically need to register your business entity, obtain necessary licenses and permits, and comply with tax regulations. The specific requirements may vary depending on the type of business and its location."},
        ]
    },
    {
        "messages": [
            {"role": "system", "content": "Welcome to the Bharat Legal GPT - Your Expert in Indian Legal Matters!"},
            {"role": "user", "content": "Can you explain the process of filing for a patent in India?"},
            {"role": "assistant", "content": "Filing for a patent in India involves several steps, including preparing a patent application, conducting a prior art search, and filing the application with the Indian Patent Office. The process can be complex and may require the assistance of a patent attorney."},
        ]
    },
    {
        "messages": [
            {"role": "system", "content": "Welcome to the Bharat Legal GPT - Your Expert in Indian Legal Matters!"},
            {"role": "user", "content": "What are the key labor laws in India that businesses should be aware of?"},
            {"role": "assistant", "content": "In India, key labor laws include the Minimum Wages Act, Industrial Disputes Act, and the Employees' Provident Funds and Miscellaneous Provisions Act, among others. These laws govern aspects of employment, wages, and workers' rights."},
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

if prompt := st.chat_input("Enter a prompt here"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    # Append the user's message to the conversation
    conversations[-1]["messages"].append({"role": "user", "content": prompt})


    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversations[-1]["messages"],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
