from qdrant_client import QdrantClient
from docling.chunking import HybridChunker
from docling.datamodel.base_models import InputFormat
from docling.document_converter import DocumentConverter
import fitz  # PyMuPDF
import base64
import os

def extract_images_from_pdf(pdf_path):
    images = []
    doc = fitz.open(pdf_path)
    for page_index in range(len(doc)):
        for img_index, img in enumerate(doc.get_page_images(page_index)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            ext = base_image["ext"]
            
            b64_image = base64.b64encode(image_bytes).decode("utf-8")
            images.append({"image": b64_image, "ext": ext, "page": page_index})
    return images


client = QdrantClient(
    url="<your Qdrant_url>", 
    api_key="<your Qdrant_key>"
)

COLLECTION_NAME = "NUTRITION_PLANNER_SUKESH"

converter = DocumentConverter(
    allowed_formats=[
        InputFormat.PDF,
        InputFormat.DOCX, 
        InputFormat.XLSX,
        InputFormat.PPTX,
        InputFormat.CSV
    ],
)

client.set_model("BAAI/bge-small-en-v1.5")
client.set_sparse_model("Qdrant/bm25")
 

def upload_file(COLLECTION_NAME ,file_path):
    result = converter.convert(file_path)
    documents, metadatas = [], []

    pdf_images = extract_images_from_pdf(file_path)
    
    for i, chunk in enumerate(HybridChunker().chunk(result.document)):
        documents.append(chunk.text)
        image_meta = {}
        for img in pdf_images:
            if img["page"] == i:  # crude match, customize logic to suit chunking
                image_meta = {"image": img["image"], "ext": img["ext"]}
                break

        metadata = chunk.meta.export_json_dict()
        metadata.update(image_meta)
        metadatas.append(metadata)
        metadatas.append(chunk.meta.export_json_dict())
        print(f"©️ Data chunking: {i + 1}")

    client.add (
        collection_name=COLLECTION_NAME,
        documents=documents,
        metadata=metadatas,
        batch_size=64,
    )  

file_path = "D:/DAVIDSON/INTERNSHIP/PROJECT 1/TESTING/Nutrient.docx"  

try:
    upload_file(COLLECTION_NAME, file_path)
    print(f"Uploaded {file_path} to Qdrant successfully!🟢")
except Exception as e:
    print(f"❌ Failed to upload: {e}")