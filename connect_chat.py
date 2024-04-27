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
        print(textwrap.dedent("""
        Logging Information: 
        - EMAIL: {EMAIL},
        - cookie_path_dir: {cookie_path_dir}
        －－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
        """).format(EMAIL=self.EMAIL, PASSWD=self.PASSWD, cookie_path_dir=self.cookie_path_dir))
        
        # 變數
        self.chatbot = None
        
    def login(self):
        # 登入
        sign = Login(self.EMAIL, self.PASSWD)
        cookies = sign.login(cookie_dir_path=self.cookie_path_dir, save_cookies=True)
        self.chatbot = hugchat.ChatBot(cookies=cookies.get_dict()) 
        
    def query(self, query):
        query_result = self.chatbot.chat(query)
        print(query_result) # or query_result.text or query_result["text"]
        
    
if __name__ == "__main__":
    
    hugging_chat_movie = HuggingChatMovie()
    hugging_chat_movie.login()
    hugging_chat_movie.query("告訴我 [overlord] 這部動漫在說什麼")
    