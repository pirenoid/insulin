import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


def parse_fasta(filename):
    sequences = []
    current_sequence = ""

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('>'):
                if current_sequence:
                    sequences.append(current_sequence)
                    current_sequence = ""
            else:
                current_sequence += line

        if current_sequence:
            sequences.append(current_sequence)

    return sequences


filename = "uniprot_sprot.fasta"
sequences = parse_fasta(filename)
print(f"Первая цепочка: {sequences[0]}")

vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(1, 3))
tfidf_matrix = vectorizer.fit_transform(sequences)

with open('tfidf_vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

np.savez_compressed('tfidf_matrix.npz', data=tfidf_matrix.data,
                   indices=tfidf_matrix.indices,
                   indptr=tfidf_matrix.indptr,
                   shape=tfidf_matrix.shape)

with open('sequence_index.pkl', 'wb') as f:
    pickle.dump(sequences, f)

print("Модель сохранена")