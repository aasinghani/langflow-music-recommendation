import streamlit as st
from langflow.load import run_flow_from_json

st.title("Langflow Chatbot")

# Function to run the Langflow chain
def run_flow(input_text):
    return run_flow_from_json(
        flow="Spotify Recommender 2.0.json",  # Update with your actual flow file
        input_value=input_text,
        fallback_to_env_vars=True,
        tweaks=None
    )

# Initialize session state for messages and model
if "langflow_model" not in st.session_state:
    st.session_state["langflow_model"] = "Spotify Recommender 2.0"  # Update if needed

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response from Langflow
    with st.chat_message("assistant"):
        response_text = ""
        response_stream = run_flow(prompt)
        
        # Assuming `response_stream` is a generator or iterable of strings
        for chunk in response_stream:
            # Convert the chunk to string if it is not already
            if isinstance(chunk, str):
                response_text += chunk
            else:
                response_text += str(chunk)
            st.markdown(response_text, unsafe_allow_html=True)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response_text})
