from sentence_transformers import SentenceTransformer

model = SentenceTransformer("paraphrase-albert-small-v2")
model.save("./models/paraphrase-albert-small-v2")
