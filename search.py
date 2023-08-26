from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from restaurant_menu import restaurant_menu
import pickle


def semantic_search(query, threshold=0.3):
    if query == '':
        return
    # find the embeddings for the query
    from build_embedding_model import get_embeddings
    query_embedding = np.array(get_embeddings(query))

    # find the similar items for the query
    return find_closest_sentences(query_embedding, threshold)


def find_closest_sentences(query_embedding, threshold=0.3):
    # Load the embeddings dictionary using pickle
    with open('embeddings.pkl', 'rb') as f:
        embeddings_dict = pickle.load(f)

    # Calculate cosine similarity between the query embedding and all embeddings
    similarities = {}
    for item, emb in embeddings_dict.items():
        similarity = cosine_similarity([emb], [query_embedding])[0][0]
        similarities[item] = similarity

    # Sort similarities in descending order
    sorted_similarities = sorted(
        similarities.items(), key=lambda x: x[1], reverse=True)

    # Retrieve the top 5 closest menu items and their similarity scores
    top_5_closest = sorted_similarities[:5]
    # Store the top 5 items and their similarity scores in an array
    result_items_with_score = []
    for item, similarity in top_5_closest:
        # print(item, " - Similarity:", similarity)
        result_items_with_score.append((item, similarity))

    return result_items_with_score


# semantic_search("what are the best sides")
