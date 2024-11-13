import streamlit as st
import openai
from openai import OpenAI
import warnings

# Suppress specific warning messages
warnings.filterwarnings("ignore", message=".*missing ScriptRunContext!*")

# Show title and description.
st.title("💬 🤖 CoPilot")
st.write(
    "This compassionate resource is designed to support those caring for loved ones affected by dementia and Alzheimer's disease."
    "\n\nWe understand the challenges you face, and we're here to help you navigate this journey with love and understanding. "
    "\nTo use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
    "\n\nThis is a personal project, I cover the costs myself, so if you happen to have an API key, I would deeply appreciate your support in using it." 
    "\n\nI understand that generating an API key may seem like an extra step, but it’s quick and easy. Your help means a lot to me and truly contributes to the sustainability of this project—thank you for being a part of it!"
)


# Ask user for their OpenAI API key or passcode
openai_api_key_passcode = st.text_input("OpenAI API Key or Passcode", type="password")

# Initialize variables
openai_api_key = None
input_flag = False



def check_openai_api_key_passcode(api_key_passcode):
    # Try using the provided input as an API key
    try:
        openai.api_key = api_key_passcode
        openai.models.list()
        return True, api_key_passcode  # Valid API key
    except openai.AuthenticationError:
        # Check if the input matches the passcode
        if api_key_passcode == st.secrets["PASSCODE"]:
            return True, st.secrets["OPENAI_API_KEY"]  # Valid passcode
        else:
            return False, None  # Invalid API key and passcode
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return False, None

if openai_api_key_passcode:
    input_flag, openai_api_key = check_openai_api_key_passcode(openai_api_key_passcode)
    if not input_flag:
        st.error(
            "Please enter a valid API key or, if you don't have one, the valid passcode provided to you.",
            icon="🔑"
        )
else:
    st.info(
        "Please add your OpenAI API key or the passcode provided to continue.",
        icon="🗝️"
    )

if input_flag:
    # Set the OpenAI API key
    # openai.api_key = openai_api_key
    client = OpenAI(api_key=openai_api_key)
    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("What's up?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
else:
    # Waiting for valid input
    pass
