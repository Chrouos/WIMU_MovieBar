from flask import Flask, request, jsonify
from connect_chat import HuggingChatMovie
from gpt_assistant import GPTAssistant
from sqlite_connect import UserSqliteConnection

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
    try: return int(result[0]), result
    except ValueError: return 3, result
    
def summarization_response(result):
    gpt_assistant = GPTAssistant()
    summary = gpt_assistant.summarization(result)
    return summary

def store_user_chat_history(line_id, query, response):
    if line_id is None or line_id == "":
        return "line_id is required"
    
    user_info_db = UserSqliteConnection(db_path="./database/", db_name="user_info.db")
    user_info_db.insert_user(
        line_id=line_id, 
        query=query, 
        response=response
    )
    return "Success Store In Database"

@app.route('/api/chat_query', methods=['POST'])
def chat_query():
    data = request.get_json()
    query = data.get('query', '')
    line_id = data.get('line_id', '')

    if not query:
        return jsonify({'error': 'Query is required'}), 400

    final_response = {
        'response': "", 
        'action': "", 
        'database_response': ""
    }
    
    try:
        #@ get the action
        action, action_result = get_the_action_select(query)
        
        response = ""
        if action == 1:
            response = query_assistant("664e16817d1eaccf3540c1ff", query)
        elif action == 2:
            response = query_assistant("66519a86045e6245ae5c8eb8", query)
        else:
            response = "抱歉，這是關於電影的助手，請問您需要搜尋什麼和電影相關的問題嗎？"
            
        final_response["response"] = summarization_response(response)
        final_response["database_response"] = store_user_chat_history(line_id=line_id, query=query, response=final_response["response"])
        final_response["action"] = action_result
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return final_response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8150)
