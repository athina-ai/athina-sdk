import numpy as np
from .openai_helper import OpenAI


# Similarity score
def _cosine_similarity_from_embeddings(e1: list[float], e2: list[float]) -> float:
    # Convert the embedding lists to numpy arrays
    v1 = np.array(e1)
    v2 = np.array(e2)

    # Calculate the dot product of the two vectors
    dot_product = np.dot(v1, v2)

    # Calculate the magnitudes of the vectors
    magnitude_v1 = np.linalg.norm(v1)
    magnitude_v2 = np.linalg.norm(v2)

    # Calculate the cosine similarity
    similarity = dot_product / (magnitude_v1 * magnitude_v2)

    return similarity


def similarity_score(str1, str2, model):
    openai = OpenAI()
    e1 = openai.get_embedding(str1, model=model)
    e2 = openai.get_embedding(str2, model=model)
    score = _cosine_similarity_from_embeddings(e1, e2)
    return score
