import os
from sentence_transformers import SentenceTransformer


def get_embedding_model():
    model_name = 'sentence-transformers/multi-qa-mpnet-base-dot-v1'
    model_path = 'ml_models/multi-qa-mpnet-base-dot-v1'
    if not os.path.exists(model_path):
        # Download the model only if it doesn't exist
        print("Downloading sentenceTransformer model....")
        model = SentenceTransformer(model_name)
        model.save(model_path)
        print("sentenceTransformer model saved....")
    else:
        # Load the model from the local file system
        print("Load sentenceTransformer model....")
        model = SentenceTransformer(model_path)
    return model

# if __name__ == "__main__":
#     print(create_embedding_model())
