import time
import pickle
from build_embedding_model import get_embeddings
from restaurant_menu import restaurant_menu

chunk_size = 3
menu_chunks = [restaurant_menu[i:i + chunk_size]
               for i in range(0, len(restaurant_menu), chunk_size)]
embeddings_dict = {}  # Dictionary to store embeddings

for chunk in menu_chunks:
    embeddings = [get_embeddings(item) for item in chunk]
    for item, emb in zip(chunk, embeddings):
        embeddings_dict[item] = emb

    # Sleep for a while to stay within the rate limits
    time.sleep(62)

# Save the embeddings dictionary using pickle
with open('embeddings.pkl', 'wb') as f:
    pickle.dump(embeddings_dict, f)

# Deserialize from the file
with open('embeddings.pkl', 'rb') as file:
    loaded_data = pickle.load(file)

print(loaded_data)
