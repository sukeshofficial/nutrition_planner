# 🥦 Nutrition Planner

**Nutrition Planner** is an AI-powered assistant designed to help users identify nutrient deficiencies and get personalized dietary advice. Using **Retrieval-Augmented Generation (RAG)** and a custom database of nutritional content, it offers science-backed recommendations based on user symptoms or deficiencies.

---

## 🌟 Features

- 💬 **Symptom-Based Queries**: Ask questions like “What should I eat for iron deficiency?” or “Which foods help with low energy?”
- 📚 **Custom Nutrition Knowledge Base**: Built using medical and nutritional datasets or documents.
- ⚡ **Fast & Contextual Retrieval**: Utilizes Qdrant for quick and relevant chunk-based search.
- 🧠 **Intelligent Answers**: Combines retrieval with a language model to deliver helpful suggestions.
- 🖥️ **User-Friendly Interface**: Built using Streamlit for easy access and clean visuals.

---

## 📁 Project Structure

```
nutrition-planner/
│
├── app.py                # Main Streamlit interface
├── rag_pipeline.py       # RAG logic (embedding, retrieval, generation)
├── nutrition_loader.py   # Loads and processes nutrition documents
├── qdrant_client.py      # Handles vector DB operations
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

## ⚙️ How It Works

1. **Upload** a nutritional knowledge base (text or PDFs).
2. The text is chunked and converted into embeddings.
3. Embeddings are stored in **Qdrant**, a vector search engine.
4. Users type symptoms/queries (e.g., “hair fall,” “weak bones”).
5. Relevant content is retrieved and passed to a language model to generate tailored advice.

---

## 🧑‍💻 Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Vector Store**: [Qdrant](https://qdrant.tech/)
- **RAG + Embeddings**: OpenRouter / OpenAI / Hugging Face
- **Backend**: Python

---

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/nutrition-planner.git
cd nutrition-planner
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Environment Variables

Create a `.env` file:

```bash
OPENROUTER_API_KEY=your_key_here
QDRANT_HOST=http://localhost:6333
```

### 4. Launch the App

```bash
streamlit run app.py
```

---

## 📷 Screenshots

*(Add some UI screenshots of your app here.)*

---

## ✅ Future Enhancements

- [ ] Add tracking of daily intake
- [ ] Integrate food database API
- [ ] Support multilingual queries
- [ ] Mobile version of the interface

---

## 📄 License

MIT License. Use and modify freely.

---

## 🙏 Acknowledgements

- [Qdrant](https://qdrant.tech/)
- [Streamlit](https://streamlit.io/)
- [OpenRouter](https://openrouter.ai/)
- [FDC USDA](https://fdc.nal.usda.gov/) (for nutritional data, if used)