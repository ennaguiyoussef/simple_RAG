"""RAG Core Logic - Separate from notebook"""
import ollama

EMBEDDING_MODEL = 'hf.co/CompendiumLabs/bge-base-en-v1.5-gguf'
LANGUAGE_MODEL = 'hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF'

VECTOR_DB = []

def load_dataset(filepath='cat-facts'):
    """Load the cat facts dataset"""
    dataset = []
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            dataset = file.readlines()
        print(f'✓ Loaded {len(dataset)} entries from {filepath}')
    except FileNotFoundError:
        print(f'✗ File {filepath} not found')
    return dataset

def add_chunk_to_database(chunk):
    """Add a chunk to the vector database with its embedding"""
    try:
        embedding = ollama.embed(model=EMBEDDING_MODEL, input=chunk)['embeddings'][0]
        VECTOR_DB.append((chunk.strip(), embedding))
    except Exception as e:
        print(f'Error adding chunk: {e}')

def initialize_database():
    """Load dataset and build vector database"""
    dataset = load_dataset()
    for i, chunk in enumerate(dataset):
        add_chunk_to_database(chunk)
        if (i + 1) % 20 == 0:
            print(f'  → Added {i+1}/{len(dataset)} chunks')
    print(f'✓ Vector database ready with {len(VECTOR_DB)} entries\n')

def cosine_similarity(a, b):
    """Calculate cosine similarity between two vectors"""
    dot_product = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x ** 2 for x in a) ** 0.5
    norm_b = sum(x ** 2 for x in b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0
    return dot_product / (norm_a * norm_b)

def retrieve(query, top_n=3):
    """Retrieve top N most relevant chunks for a query"""
    try:
        query_embedding = ollama.embed(model=EMBEDDING_MODEL, input=query)['embeddings'][0]
    except Exception as e:
        print(f'Error embedding query: {e}')
        return []

    similarities = []
    for chunk, embedding in VECTOR_DB:
        similarity = cosine_similarity(query_embedding, embedding)
        similarities.append((chunk, similarity))

    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:top_n]

def chat_with_rag(input_query):
    """Get RAG response for a query"""
    if not VECTOR_DB:
        return "Error: Vector database is empty. Please initialize it first."

    retrieved_knowledge = retrieve(input_query)

    if not retrieved_knowledge:
        return "I couldn't find relevant information in the knowledge base."

    instruction_prompt = f'''You are a helpful chatbot about cats. You have access to a knowledge base about cats.
Use ONLY the following pieces of context to answer the question. 
If the answer is not in the context, say "I don't know" or "This information is not available in my knowledge base."
Do NOT make up any new information.

Context:
{chr(10).join([f'- {chunk}' for chunk, similarity in retrieved_knowledge])}

Answer the question clearly and concisely.'''

    try:
        response = ollama.chat(
            model=LANGUAGE_MODEL,
            messages=[
                {'role': 'system', 'content': instruction_prompt},
                {'role': 'user', 'content': input_query},
            ],
            stream=False,
        )
        return response['message']['content']
    except Exception as e:
        return f"Error generating response: {str(e)}"

