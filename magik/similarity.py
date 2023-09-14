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


def levenshtein_distance(str1, str2):
    m, n = len(str1), len(str2)
    # Create a matrix to store the distances
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Initialize the first row and first column
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    # Calculate the distance
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i]
                                   [j - 1], dp[i - 1][j - 1])

    return dp[m][n]
