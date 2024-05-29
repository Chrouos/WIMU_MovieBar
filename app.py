from flask import Flask, request, jsonify
from connect_chat import HuggingChatMovie
from gpt_assistant import GPTAssistant

app = Flask(__name__)

def query_assistant(assistant_id, query):
    hugging_chat_movie = HuggingChatMovie()
    hugging_chat_movie.change_assistant(_assistant_id=assistant_id)
    response = hugging_chat_movie.query(_query=query, _web_search=True)
    # hugging_chat_movie.logout()
    return response

def get_the_action_select(query):
    gpt_assistant = GPTAssistant()
    result = gpt_assistant.select_action(query)
    print("action selector", result)
    try: return int(result[0]), result
    except ValueError: return 3, result
    
def summarization(result):
    gpt_assistant = GPTAssistant()
    summary = gpt_assistant.summarization(result)
    return summary

@app.route('/api/chat_query', methods=['POST'])
def chat_query():
    data = request.get_json()
    query = data.get('query', '')

    if not query:
        return jsonify({'error': 'Query is required'}), 400

    try:
        #@ get the action
        action, result = get_the_action_select(query)
        
        response = ""
        if action == 1:
            response = query_assistant("664e16817d1eaccf3540c1ff", query)
        elif action == 2:
            response = query_assistant("66519a86045e6245ae5c8eb8", query)
        else:
            response = "抱歉，這是關於電影的助手，請問您需要搜尋什麼和電影相關的問題嗎？"
            
        response_after_summarization = summarization(response)
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'response': str(response_after_summarization), 'action': result})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8150)
