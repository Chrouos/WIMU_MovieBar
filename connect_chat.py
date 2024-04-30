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
        for source in query_result.web_search_sources:
            print(textwrap.dedent("""
            Query Information: 
            - Link: {Link},
            - Title: {Title},
            - hostname: {Hostname}
            －－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
            """).format(Link=source.link, Title=source.title, Hostname=source.hostname))
        
        print(query_result)
        
            
    def change_assistant(self, _assistant_id):
        try:
            self.chatbot.new_conversation(assistant=_assistant_id, switch_to = True)
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
        
    
if __name__ == "__main__":
    
    hugging_chat_movie = HuggingChatMovie()
    # hugging_chat_movie.output_assistant_list()
    hugging_chat_movie.change_assistant(_assistant_id="66207bb286188d2c9787a941")
    hugging_chat_movie.query(
        _query="我想知道 2019 年有什麼好看的英雄電影，我希望裡面有蜘蛛人出現", 
        _web_search=True
    )
    