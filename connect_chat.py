import os
from dotenv import load_dotenv
import textwrap

from hugchat import hugchat
from hugchat.login import Login

class HuggingChatMovie:
    def __init__(self) -> None:
        
        # 載入環境變數
        load_dotenv()

        # 從 .env 檔案中讀取變數
        self.EMAIL = os.getenv('EMAIL')
        self.PASSWD = os.getenv('PASSWD')
        self.cookie_path_dir = os.getenv('cookie_path_dir')
        self.chatbot = None
        
        #- Login & Output Information.
        self.login()
        print(textwrap.dedent("""
        Logging Information: 
        - EMAIL: {EMAIL},
        - cookie_path_dir: {cookie_path_dir}
        －－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
        """).format(EMAIL=self.EMAIL, PASSWD=self.PASSWD, cookie_path_dir=self.cookie_path_dir))
        
    def login(self):
        # 登入
        sign = Login(self.EMAIL, self.PASSWD)
        cookies = sign.login(cookie_dir_path=self.cookie_path_dir, save_cookies=True)
        self.chatbot = hugchat.ChatBot(cookies=cookies.get_dict()) 
        
    def query(self, _query, _web_search=False):
        
        query_result = self.chatbot.query(_query, web_search=_web_search)
        print(query_result)
        for source in query_result.web_search_sources:
            print(source.link)
            print(source.title)
            print(source.hostname)
            
    def change_assistant(self, _assistant_name):
        try:
            assistant = self.chatbot.search_assistant(assistant_name=_assistant_name)
            self.chatbot.new_conversation(assistant=assistant, switch_to=True)
            print(f"Now you assigned assistant: {assistant}")
        except Exception as e:
            print(f"[change_assistant] error in: {e}")
        
    
if __name__ == "__main__":
    
    hugging_chat_movie = HuggingChatMovie()
    
    hugging_chat_movie.change_assistant(_assistant_name="Movie and TV Recommendations")
    hugging_chat_movie.query(
        _query="告訴我 [overlord] 這部動漫在說什麼", 
        _web_search=True
    )
    