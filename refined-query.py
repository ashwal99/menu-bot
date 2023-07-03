import openai

from creds import OPENAI_API_KEY

def generate_refined_query(conversation, latest_query):
    # Set up OpenAI API credentials
    openai.api_key = OPENAI_API_KEY

    # Define the prompt for generating the refined query
    prompt = f"Conversation:\n{conversation}\n\nLatest Query:\n{latest_query}\n\nAssistant: A refined query is a more specific question or statement that includes all the necessary information to answer the latest query. It provides additional context or details that help address the specific query. Please generate a refined query based on the conversation and the latest query below.\n\nUser: {latest_query}\nRefined Query:"

    # Generate the refined query using the Language Model
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=50,
        temperature=0,
        n=1,
        stop=None,
        echo=True
    )

    # Extract the refined query from the API response
    refined_query = response.choices[0].text.strip().split('Refined Query:')[1].strip()

    return refined_query