from flask import Flask, request, jsonify
from connect_chat import HuggingChatMovie

app = Flask(__name__)

def query_assistant(assistant_id, query):
    hugging_chat_movie = HuggingChatMovie()
    hugging_chat_movie.change_assistant(_assistant_id=assistant_id)
    response = hugging_chat_movie.query(_query=query, _web_search=True)
    hugging_chat_movie.logout()
    return response

@app.route('/api/chat_query', methods=['POST'])
def chat_query():
    data = request.get_json()
    query = data.get('query', '')

    if not query:
        return jsonify({'error': 'Query is required'}), 400

    try:
        response_all = query_assistant("664e16817d1eaccf3540c1ff", query)
        response_domain = query_assistant("66519a86045e6245ae5c8eb8", query)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({
        'response_all': str(response_all),
        'response_domain': str(response_domain)
    })

if __name__ == '__main__':
    app.run(debug=True, port=8150)
