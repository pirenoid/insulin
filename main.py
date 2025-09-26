import pickle
import numpy as np
from scipy.sparse import csr_matrix
import argparse
from sklearn.metrics.pairwise import cosine_similarity


def load_model():
    with open('tfidf_vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)

    loaded = np.load('tfidf_matrix.npz')
    tfidf_matrix = csr_matrix((loaded['data'], loaded['indices'], loaded['indptr']), shape=loaded['shape'])

    with open('sequence_index.pkl', 'rb') as f:
        sequences = pickle.load(f)

    return vectorizer, tfidf_matrix, sequences


def find_similar_sequences(user_sequence, vectorizer, tfidf_matrix, sequences, top_k=1000):
    user_vector = vectorizer.transform([user_sequence])

    similarities = cosine_similarity(user_vector, tfidf_matrix)

    top_indices = similarities.argsort()[0][-top_k:][::-1]

    results = []
    for idx in top_indices:
        results.append({'sequence': sequences[idx], 'similarity': similarities[0, idx]})

    return results


def save_sequences_to_file(sequences, filename="similar_sequences.txt"):
    with open(filename, 'w', encoding='utf-8') as f:
        for sequence in sequences:
            f.write(sequence['sequence'] + '\n')
    return filename


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('seq', type=str, help='Цепочка для поиска')
    args = parser.parse_args()

    with open('input.txt', 'w', encoding='utf-8') as f:
        f.write(args.seq)

    print("Загрузка модели")
    vectorizer, tfidf_matrix, sequences = load_model()
    print(f"Модель загружена")

    print("Поиск похожих")
    similar_sequences = find_similar_sequences(args.seq, vectorizer, tfidf_matrix, sequences)
    output_filename = save_sequences_to_file(similar_sequences)
    for i, result in enumerate(similar_sequences[:10]):
        print(f"{i + 1}. Сходство: {result['similarity']:.4f}")
        print(f"   Последовательность: {result['sequence']}")
    print('Похожие цепочки сохранены в similar_sequences.txt')