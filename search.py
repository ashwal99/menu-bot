from sklearn.metrics.pairwise import cosine_similarity
from build_embedding_model import get_embedding_model
import numpy as np
from restaurant_menu import restaurant_menu


def semantic_search(query, threshold=0.3):
    if query == '':
        return
    # find the embeddings for the query
    embedding_model = get_embedding_model()
    query_embedding = embedding_model.encode(
        query, batch_size=10)

    # find the similar items for the query
    return find_closest_sentences(query_embedding, threshold)


def find_closest_sentences(query_embedding, threshold=0.3):
    sentence_embeddings = np.load('embeddingsForMenu.npy')
    # Calculate cosine similarity between query embedding and sentence embeddings
    similarity_scores = cosine_similarity(
        query_embedding.reshape(1, -1), sentence_embeddings)[0]

    # Find the indices of closest sentences based on similarity scores
    closest_indices = np.argsort(similarity_scores)[::-1]

    # Get the closest sentences and their similarity scores
    closest_sentences = [restaurant_menu[idx] for idx in closest_indices]
    similarity_scores = similarity_scores[closest_indices]
    # print('-----------------------------------------------')
    # Display the closest sentences and their similarity scores
    result_items_with_score = []
    for sentence, score in zip(closest_sentences, similarity_scores):
        # print(f"Sentence: {sentence}\nCosine Similarity: {score}\n")
        if score >= threshold:
            result_items_with_score.append((sentence, score))

    # print(result_items_with_score)
    return result_items_with_score


# semantic_search("what are the best sides")
