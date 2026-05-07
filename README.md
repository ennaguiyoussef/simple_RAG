# 🐱 Cat Facts RAG Chatbot

Une application de chatbot alimentée par un système RAG (Retrieval-Augmented Generation) pour répondre à des questions sur les chats.

## Architecture

```
simple_RAG/
├── app.py                    # Flask API
├── rag_core.py              # Logique RAG isolée
├── rag_system.ipynb         # Notebook pour tests/développement
├── cat-facts                # Base de connaissances
├── requirements.txt         # Dépendances Python
└── frontend/
    └── src/
        ├── chatbot.jsx      # Composant React principal
        ├── chatbot.css      # Styles
        └── ...
```

## Prérequis

- **Python 3.8+**
- **Node.js 16+**
- **Ollama** (pour les embeddings et génération)

## Installation

### 1️⃣ Backend (Flask)

```bash
# Installer les dépendances Python
pip install -r requirements.txt
```

### 2️⃣ Frontend (React)

```bash
cd frontend

# Installer les dépendances Node
npm install
```

## Lancer l'application

### Terminal 1 - Serveur Flask

```bash
python app.py
```

Vous devriez voir :
```
✓ RAG Chatbot API Ready!
📍 API running at: http://localhost:5000
```

### Terminal 2 - Serveur React

```bash
cd frontend
npm start
```

L'application s'ouvrira automatiquement à `http://localhost:3000`

## Utilisation

1. **Ouvrir l'interface** : http://localhost:3000
2. **Poser une question** sur les chats
3. **Obtenir une réponse** basée sur la base de connaissances

### Exemples de questions

- "How high can a cat jump?"
- "What is the oldest cat on record?"
- "Why do cats hate water?"
- "What is a group of cats called?"
- "How many teeth does a cat have?"

## API Endpoints

### `POST /chat`

Envoie une question et reçoit une réponse RAG.

**Request:**
```json
{
  "message": "How many teeth does a cat have?"
}
```

**Response:**
```json
{
  "success": true,
  "message": "How many teeth does a cat have?",
  "answer": "Grown cats have 30 teeth. Kittens have about 26 temporary teeth..."
}
```

### `GET /health`

Vérifie que l'API fonctionne.

**Response:**
```json
{
  "status": "ok",
  "message": "RAG Chatbot API is running"
}
```

## Structure du projet

### Backend

- **app.py** : Serveur Flask avec l'endpoint `/chat`
- **rag_core.py** : Logique RAG complète (embeddings, retrieval, génération)
- **rag_system.ipynb** : Notebook Jupyter pour tester/développer

### Frontend

- **chatbot.jsx** : Composant React principal avec :
  - Historique des messages
  - Animations fluides
  - Gestion du loading
  - Support de Enter pour envoyer

- **chatbot.css** : Design moderne avec :
  - Gradient coloré
  - Animations d'entrée
  - Responsive design
  - Typing indicator

## Configuration

### Modèles Ollama

Modifiables dans `app.py` ou `rag_core.py` :

```python
EMBEDDING_MODEL = 'hf.co/CompendiumLabs/bge-base-en-v1.5-gguf'
LANGUAGE_MODEL = 'hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF'
```

### Base de connaissances

Le fichier `cat-facts` contient environ 150 faits sur les chats. Pour ajouter plus de données, simplement ajouter des lignes au fichier.

## Troubleshooting

### "Error connecting to server"

- Vérifier que le serveur Flask tourne : `python app.py`
- Vérifier que `http://localhost:5000/health` retourne ok

### "Module not found: Flask"

```bash
pip install -r requirements.txt
```

### Les embeddings sont lents

C'est normal ! Les embeddings peuvent prendre du temps la première fois. Ollama va télécharger le modèle.

## Performance

- **Initialisation** : ~30 secondes (embedding 150 chunks)
- **Query** : ~2-5 secondes par question
- **Frontend** : Réactif et fluide

## Améliorations possibles

- [ ] Persistance des messages (LocalStorage/DB)
- [ ] Support de plusieurs langues
- [ ] Admin panel pour gérer la base de connaissances
- [ ] Rate limiting
- [ ] Authenticication utilisateur
- [ ] Dark mode
- [ ] Export/Import de conversations

## Développement

### Tester l'API

```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is a group of cats called?"}'
```

### Modifier les styles

Éditer `frontend/src/chatbot.css` pour personnaliser l'interface.

## License

MIT

## Auteur

RAG Chatbot Project 🐱

