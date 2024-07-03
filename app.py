# app.py
from flask import Flask, request, jsonify
import openai
import pymongo
from config import OPENAI_API_KEY, MONGO_URI

app = Flask(__name__)

# Set up OpenAI
openai.api_key = OPENAI_API_KEY

# Set up MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client.llm_responses
collection = db.responses

@app.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    user_query = data.get('query')

    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    try:
        # Generate response using OpenAI's GPT-4 API (example, replace with appropriate model)
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_query}
            ]
        )
        answer = response['choices'][0]['message']['content'].strip()

        # Save the response to MongoDB
        result = collection.insert_one({"query": user_query, "response": answer})

        return jsonify({"response": answer}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/store', methods=['POST'])
def store():
    data = request.get_json()
    query = data.get('query')
    response = data.get('response')

    if not query or not response:
        return jsonify({"error": "Query and response must be provided"}), 400

    try:
        # Save the query and response to MongoDB
        result = collection.insert_one({"query": query, "response": response})

        return jsonify({"message": "Data stored successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


