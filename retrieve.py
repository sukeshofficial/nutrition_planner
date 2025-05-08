import streamlit as st
import pyttsx3
from qdrant_client import QdrantClient
from response import token
import re
import fitz  # PyMuPDF

def extract_images_from_pdf(pdf_path):
    images = []
    doc = fitz.open(pdf_path)
    for i in range(len(doc)):
        for img in doc.get_page_images(i):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            images.append((image_bytes, image_ext))
    return images


def remove_emojis(text):
    emoji_pattern = re.compile(  
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002700-\U000027BF"  # Dingbats
        "\U000024C2-\U0001F251" 
        "]+",
        flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', text)


client = QdrantClient(
    url = "<your Qdrant_url>", 
    api_key = "<your Qdrant_key>",
    check_compatibility = False
)

client.set_model("BAAI/bge-small-en-v1.5")
client.set_sparse_model("Qdrant/bm25")
COLLECTION_NAME = "NUTRITION_PLANNER_MAHIMA"

st.set_page_config(
    page_title = "Nutrition Planner Assistant", 
    page_icon = "🥕"
)
st.title("🥕 Nutrition Planner Assistant")

st.sidebar.header("⚙️ Settings")
rate = st.sidebar.slider("🔊 Speech Rate", 100, 200, 125)
voice_gender = st.sidebar.radio("🔊 Voice", ["Male","Female"])
enable_voice = st.sidebar.checkbox("Enable Voice Output", value=True)

if "history" not in st.session_state:
    st.session_state.history = []

question = st.chat_input("Ask a question about the product manual...")

if question:
    with st.chat_message("user"):
        st.write(question)

    st.info("🔎 Searching product manual...")

    results = client.query(
        collection_name=COLLECTION_NAME,
        query_text=question,
        limit=5,
    )

    context = "\n".join([r.document for r in results])

    prompt = f"""
        Context: {context}
        Question: {question}
        Based on the context provided, answer the question. Give me as a plain text, don't use md format.
    """

    with st.chat_message("assistant"):
        placeholder = st.empty()
        final_output = ""

        with st.spinner("🧠 Thinking..."):
            for tok in token(prompt, model="gpt-4o-mini"):
                final_output += tok
                placeholder.markdown(final_output)

        st.session_state.history.append((question, final_output))
        
        for res in results:
            meta = res.metadata
            if "image" in meta:
                import base64
                from PIL import Image
                import io

                image_bytes = base64.b64decode(meta["image"])
                image = Image.open(io.BytesIO(image_bytes))
                st.image(image, caption="📸 Related Image from Document")
                break

        if enable_voice:
            clean_output = remove_emojis(final_output)
            engine = pyttsx3.init()
            engine.setProperty('rate', rate)
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[1].id if voice_gender == "Female" else voices[0].id)
            engine.say(clean_output)
            engine.runAndWait()


if st.session_state.history:
    st.markdown("---")
    st.subheader("🕘 Previous Questions")
    for q, a in reversed(st.session_state.history[-3:]):
        with st.expander(f"🗨️ Q: {q}"):
            st.write(a)

st.markdown("---")