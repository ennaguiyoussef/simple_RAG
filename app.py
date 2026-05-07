import ollama
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

EMBEDDING_MODEL = 'hf.co/CompendiumLabs/bge-base-en-v1.5-gguf'
LANGUAGE_MODEL = 'hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF'

VECTOR_DB = []

def load_dataset():
    with open('cat-facts' , 'r' , encoding='UTF-8') as file:
        dataset = file.readlines()
    return dataset

def add_chunk_to_database(chunk):
    embedding = ollama.embed(
        model=EMBEDDING_MODEL,
        input=chunk
    )['embeddings'][0]
    VECTOR_DB.append((chunk , embedding))

def cosine_similarity(a , b):
    dot_product = sum([x*y for x,y in zip(a,b)])
    norm_a = sum([x ** 2 for x in a]) ** 0.5
    norm_b = sum([x ** 2 for x in b]) ** 0.5
    return dot_product / (norm_a*norm_b)

def retrieve(query , top_n = 3):
    query_embedding = ollama.embed(
        model=EMBEDDING_MODEL,
        input=query
    )['embeddings'][0]
    similarities = []
    for chunk , embedding in VECTOR_DB:
        similarity = cosine_similarity(query_embedding , embedding)
        similarities.append((chunk , similarity))
    similarities.sort(key=lambda x: x[1] , reverse=True)
    return similarities[:top_n]

def chat_with_rag(input_query):
    retrieved_knowledge = retrieve(input_query)

    instruction_prompt = f''' You are a helpful chatbot.
                              Use only the following pieces of context to answer the question. 
                              Say I don't know when you not find the response. 
                              Don't make up any new information:
                              {'\n'.join([f' - {chunk}' for chunk, similarity in retrieved_knowledge])}
                          '''
    response = ollama.chat(
        model=LANGUAGE_MODEL,
        messages=[
            {'role': 'system' , 'content': instruction_prompt},
            {'role': 'user' , 'content': input_query}
        ],
        stream=False
    )
    return response['message']['content']

@app.route("/chat" , methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Missing 'message' field"}), 400

    user_message = data["message"].strip()
    
    if not user_message:
        return jsonify({"error": "Message cannot be empty"}), 400

    answer = chat_with_rag(user_message)
    return jsonify({
        "success": True,
        "message": user_message,
        "answer": answer
    })

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok", "message": "RAG Chatbot API is running"})

if __name__ == "__main__":
    print("🚀 Starting RAG Chatbot Server...\n")
    dataset = load_dataset()
    print(f'✓ Loaded {len(dataset)} entries')
    
    for i, chunk in enumerate(dataset):
        add_chunk_to_database(chunk)
        if (i + 1) % 20 == 0:
            print(f'  → Added {i+1}/{len(dataset)} chunks')
    
    print(f'✓ Vector database ready with {len(VECTOR_DB)} entries\n')
    print("=" * 50)
    print("✓ RAG Chatbot API Ready!")
    print("=" * 50)
    print("📍 API running at: http://localhost:5000")
    print("📍 Endpoint: POST /chat")
    print("=" * 50 + "\n")
    
    app.run(host="0.0.0.0" , port=5000 , debug=True)
