import os
import shutil
from dotenv import load_dotenv
import textwrap

from hugchat import hugchat
from hugchat.login import Login

class HuggingChatMovie:
    def __init__(self, is_show=False) -> None:
        
        # 載入環境變數
        load_dotenv()

        # 從 .env 檔案中讀取變數
        self.EMAIL = os.getenv('EMAIL')
        self.PASSWD = os.getenv('PASSWD')
        self.cookie_path_dir = os.getenv('cookie_path_dir')
        self.chatbot = None
        
        #- Login & Output Information.
        self.login()
        if is_show :
            print(textwrap.dedent("""
            Logging Information: 
            - EMAIL: {EMAIL},
            - cookie_path_dir: {cookie_path_dir}
            －－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
            """).format(EMAIL=self.EMAIL, PASSWD=self.PASSWD, cookie_path_dir=self.cookie_path_dir))
        
    def login(self):
        try:
            # 登入
            sign = Login(self.EMAIL, self.PASSWD)
            cookies = sign.login(cookie_dir_path=self.cookie_path_dir, save_cookies=True)
            self.chatbot = hugchat.ChatBot(cookies=cookies.get_dict()) 
            
            print("[login] Successed.")
        except Exception as e:
            print(f"[login] error in: {e}")
        
    def query(self, _query, _web_search=False):
        
        query_result = self.chatbot.query(_query, web_search=_web_search)
        print(textwrap.dedent(f"""
            - Query:\n {_query}
            
            - Response:\n {query_result}
        """))
        
        # other_information = ""
        # for source in query_result.web_search_sources:
        #     current_info = textwrap.dedent("""
        #     Query Information: 
        #     - Link: {Link},
        #     - Title: {Title},
        #     －－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
        #     """).format(Link=source.link, Title=source.title)
        #     print(current_info)
            
        #     other_information += current_info
        
        return query_result
        
            
    def change_assistant(self, _assistant_id):
        try:
            self.chatbot.new_conversation(assistant=_assistant_id, switch_to = True)
            print(f"Change Assistant to: {_assistant_id}")
            # assistant = self.chatbot.search_assistant(assistant_name=_assistant_id)
            # self.chatbot.new_conversation(assistant=assistant, switch_to=True)
            # print(f"Now you assigned assistant: {assistant}")
        except Exception as e:
            print(f"[change_assistant] error in: {e}")
            
    def output_assistant_list(self, page=0):
        assistant_list = self.chatbot.get_assistant_list_by_page(page=page)
        for assistant in assistant_list:
            print(textwrap.dedent(f"""
            Assistant ID: {assistant.assistant_id}
            - Author: {assistant.author}
            - Name: {assistant.name}
            - Model Name: {assistant.model_name}
            －－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
            """))
            
        return assistant_list
    
    def logout(self):
        cookies_path = self.cookie_path_dir
        
        # 刪除 cookies 檔案夾中的所有檔案
        if os.path.exists(cookies_path):
            shutil.rmtree(cookies_path)
            
        # 重新建立空的 cookies 檔案夾
        os.makedirs(cookies_path)   
    
if __name__ == "__main__":
    print("start to connect the hugging chat API.")
    
    hugging_chat_movie_all = HuggingChatMovie()
    hugging_chat_movie_all.change_assistant(_assistant_id="664e16817d1eaccf3540c1ff")
    response_response_all = hugging_chat_movie_all.query(
        _query="告訴我歌喉讚的主角是誰?", 
        _web_search=True
    )
    print("response_response_all:\n", response_response_all, "\n")
    # hugging_chat_movie_all.logout()

    # hugging_chat_movie_domain = HuggingChatMovie()
    # hugging_chat_movie_domain.change_assistant(_assistant_id="66519a86045e6245ae5c8eb8")
    # response_response_domain = hugging_chat_movie_domain.query(
    #     _query="告訴我歌喉讚的主角是誰?", 
    #     _web_search=True
    # )
    # print("response_response_domain:\n", response_response_domain)
    # hugging_chat_movie_domain.logout()
    
    
    print("End to use.")