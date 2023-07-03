
import streamlit as st
import pandas as pd
import openai


# Set up OpenAI API credentials
openai.api_key = "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"

# Define the menu as a list of strings
menu = [
    "Margherita : Classic pizza with tomato sauce and mozzarella cheese : Veg : Veg Pizza : #vegan, #chefSpecial",
    "Pepperoni : Pizza with tomato sauce, mozzarella, and pepperoni : Non-veg : NV Pizza : #spicy, #recommended",
    "Caesar Salad : Romaine lettuce, croutons, Parmesan cheese, Caesar dressing : Veg : Specialty : #dairyFree, #wantToRepeat",
    "BBQ Chicken : Pizza with barbecue sauce, chicken, and onions : Non-veg : NV Pizza : #specialtyChicken, #mealFor2",
    "Garlic Bread : Sliced baguette with garlic butter and Parmesan : Veg : Sides : #new, #sides",
    "Chicken Alfredo : Fettuccine with creamy Alfredo sauce and chicken : Non-veg : Meals and combos : #containsDairy, #mealFor2",
    "Vegan Burger : Plant-based burger patty with lettuce, tomato, and onion : Veg : Meals and combos : #guiltFree, #vegan, #mealFor2",
    "Tandoori Chicken : Chicken marinated in Indian spices and grilled : Non-veg : Specialty : #spicy, #recommended, #new",
    "Caprese Salad : Fresh mozzarella, tomato, and basil drizzled with balsamic : Veg : Specialty : #wantToRepeat, #dairyFree",
    "Hawaiian Pizza : Pizza with tomato sauce, mozzarella, ham, and pineapple : Non-veg : NV Pizza : #new, #recommended",
    "Margherita Extra : Margherita pizza with extra cheese and basil : Veg : Veg Pizza : #wantToRepeat",
    "Buffalo Wings : Deep-fried chicken wings served with hot sauce and blue cheese : Non-veg : Sides : #spicy, #sides,#specialtyChicken, #new",
    "Greek Salad : Lettuce, tomato, cucumber, feta cheese, and Kalamata olives : Veg : Specialty : #wantToRepeat, #dairyFree, #glutenFree"
]

# Create a DataFrame from the menu
menu_data = []
for item in menu:
    item_data = item.split(" : ")
    menu_data.append(item_data)
menu_df = pd.DataFrame(menu_data, columns=["Item", "Description", "Type", "Category", "Tags"])

# Initialize chat history
chat_history = []

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
    # Add user input to chat history
    st.session_state.chat_history.append({"role": "user", "content": st.session_state.input_message})

    # Generate response from GPT model
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.chat_history
    )

    # Add model response to chat history
    st.session_state.chat_history.append({"role": "assistant", "content": response['choices'][0]['message']['content']})

    # Calculate and display the number of tokens used
    num_tokens = response["usage"]["total_tokens"]
    st.sidebar.subheader("Tokens Used")
    st.sidebar.write(f"{num_tokens} tokens used by the OpenAI API.")

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
