from flask import Flask, request, jsonify
from flask_cors import CORS
from pydantic import BaseModel
import asyncio
from main import OwnGPT  # Assuming your main logic is in main.py

app = Flask(__name__)
CORS(app)  # Allow CORS for local development

class QueryRequest(BaseModel):
    query: str

inst = OwnGPT()

@app.route('/ask', methods=['POST'])
def ask():
    query_request = request.get_json()
    query = query_request.get('query', '')
    
    urls = inst.get_google_search_urls(query=query)
    texts = asyncio.run(inst.extract_and_clean_text(urls))
    inst.store_texts_in_vector_db(texts)
    context = asyncio.run(inst.retrieve_relevant_context(query))
    response = asyncio.run(inst.generate_response(query=query, context=context))
    
    return jsonify({"response": response})
@app.route("/health", methods=['GET'])
def health():
    return jsonify({"status": "healthy"})
c
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000,debug = True)