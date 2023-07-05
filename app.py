
import streamlit as st
import pandas as pd
import openai

from creds import OPENAI_API_KEY
from refined_query import generate_refined_query
from restaurant_menu import restaurant_menu


# Set up OpenAI API credentials
openai.api_key = OPENAI_API_KEY

# Define the menu as a list of strings
menu = restaurant_menu

# Create a DataFrame from the menu
menu_data = []
for item in menu:
    item_data = item.split(" : ")
    menu_data.append(item_data)
menu_df = pd.DataFrame(menu_data, columns=["Item", "Description", "Type", "Category", "Tags"])

# Initialize chat history
chat_history = [{'role':'system', 'content':"""
You are OrderBot, an automated service to collect orders for a pizza restaurant. \
You first greet the customer, then collects the order, \
and then asks if it's a pickup or delivery. \
You wait to collect the entire order, then summarize it and check for a final \
time if the customer wants to add anything else. \
If it's a delivery, you ask for an address. \
Finally you collect the payment.\
Make sure to clarify all options, extras and sizes to uniquely \
identify the item from the menu.\
You respond in a short, very conversational friendly style. \
"""}]

chat_history.append({'role':'system', 'content':f'''The menu includes \
{menu}
'''})
# Streamlit application layout
st.title("Restaurant Waiter Chatbot")

st.subheader("Menu")
st.table(menu_df)

st.subheader("Chat")

# Load previous conversation from SessionState or initialize if not available
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
if 'input_message' not in st.session_state:
    st.session_state['input_message'] = ''

# Display chat history
chat_container = st.empty()

# Custom CSS for chat scroll and user input
st.markdown(
    """
    <style>
    .chat-container {
        max-height: 600px;
        overflow-y: auto;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 5px;
    }
    .user-input {
        margin-top: 10px;
    }
    .user {
        background-color: #052942;
        padding: 5px;
        margin-bottom: 5px;
        border-radius: 5px;
    }
    .assistant {
        background-color: #0f6d0f;
        padding: 5px;
        margin-bottom: 5px;
        border-radius: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to handle user input
def onClick():
    # Generate refined query from chat history and latest query
    refined_query = generate_refined_query(st.session_state.chat_history, st.session_state.input_message)

    # Add user input to chat history
    st.session_state.chat_history.append({"role": "user", "content": st.session_state.input_message})

    # Initialise messages
    messages = [{'role':'system', 'content':"""
    You are OrderBot, an automated service to collect orders for a pizza restaurant. \
    You first greet the customer, then collects the order, \
    and then asks if it's a pickup or delivery. \
    You wait to collect the entire order, then summarize it and check for a final \
    time if the customer wants to add anything else. \
    If it's a delivery, you ask for an address. \
    Finally you collect the payment.\
    Make sure to clarify all options, extras and sizes to uniquely \
    identify the item from the menu.\
    You respond in a short (max 20 words), very conversational friendly style. \
    Dont talk about to many items at once. \
    """}]

    messages.append({'role':'system', 'content':f'''The menu includes \
    {menu}
    '''})

    messages.append({"role": "user", "content": refined_query})


    # Generate response from GPT model
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens=50,
        messages=messages
    )

    # Add model response to chat history
    st.session_state.chat_history.append({"role": "assistant", "content": response['choices'][0]['message']['content']})

    # Calculate and display the number of tokens used
    num_tokens = response["usage"]["total_tokens"]
    st.sidebar.subheader("Tokens Used")
    st.sidebar.write(f"{num_tokens} tokens used by the OpenAI API.")

    # Display the refined query in the sidebar
    st.sidebar.subheader("Refined Query")
    st.sidebar.write(refined_query)

# Render chat history with scrolling
chat_html = ""
for chat in st.session_state.chat_history:
    role = chat["role"]
    content = chat["content"]
    if role == "user":
        chat_html += f'<div class="user">{content}</div>'
    elif role == "assistant":
        chat_html += f'<div class="assistant">{content}</div>'

# Render chat history with scrolling
chat_container.markdown(
    f'<div class="chat-container">{chat_html}</div>',
    unsafe_allow_html=True
)

# User input form
st.session_state.input_message = st.text_input("User input:", key="user_input")
submit_button = st.button("Submit", on_click=onClick)
