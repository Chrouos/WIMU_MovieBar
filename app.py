from flask import Flask, request, jsonify
from connect_chat import HuggingChatMovie

app = Flask(__name__)

@app.route('/api/chat_query', methods=['POST'])
def chat_query():
    data = request.get_json()
    query = data.get('query', '')
    
    print("query:", query)
    if not query:
        return jsonify({'error': 'Query is required'}), 400
    
    response_query = hugging_chat_movie.query(
        _query=query, 
        _web_search=True
    )
    print(response_query)

    return {"response": str(response_query)}


if __name__ == '__main__':
    
    hugging_chat_movie = HuggingChatMovie()
    hugging_chat_movie.change_assistant(_assistant_id="66207bb286188d2c9787a941")
    
    app.run(debug=True)
