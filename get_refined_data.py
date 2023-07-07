import numpy as np
from numpy.linalg import norm


def getTopKItems(model,embeddings, sentences, query, threshold=0.4):
  query_embedding = model.encode(query)
  arr = []
  # run semantic similarity search
  print("Semantic Query:" + query)
  for e, s in zip(embeddings, sentences):
      arr.append([s,cosine_similarity(e, query_embedding)])

  topK = [item for item in sorted(arr, key=lambda x: -x[1]) if item[1] > threshold]
  return topK[:5] if len(topK)> 5 else topK

# define our distance metric
def cosine_similarity(a, b):
    return np.dot(a, b)/(norm(a)*norm(b))