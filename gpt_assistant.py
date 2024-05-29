
from dotenv import load_dotenv
from openai import OpenAI
from Prompt import base_prompt_to_select_action 
import os

class GPTAssistant():
    def __init__(self) -> None:
        
        load_dotenv()
        GPT_KEY = os.getenv('GPT_KEY')
        
        self.client = OpenAI(
            api_key=GPT_KEY
        )
        
    def select_action(self, query):
        
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo-0301",
            messages=[
                {"role": "system", "content": ""},
                {"role": "user", "content": base_prompt_to_select_action + query}
            ]
        )
        
        return completion.choices[0].message.content
        
if __name__ == "__main__":
    gpt_assistant = GPTAssistant()
    result = gpt_assistant.select_action(query="Tell me about the 'overlord' this anime work is talking about.")
    print(result)
