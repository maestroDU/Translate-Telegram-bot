from requests import Session
import json

headers = {"Content-Type": "application/json", "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"}
url = "https://translate.argosopentech.com/translate"


class Translator:
    def __init__(self) -> None:
        self.session = Session()
        self.session.headers = headers
        
    def ru_to_en(self, text: str) -> str:
        body = {
            'q' : text,
            'source' : 'ru',
            'target' : 'en',
            'format' : 'text',
            'api_key' : ''
        }
        response = json.loads(self.session.post(url=url, data=json.dumps(body)).text)
        return response['translatedText']
    
    def en_to_ru(self, text: str) -> str:
        body = {
            'q' : text,
            'source' : 'en',
            'target' : 'ru',
            'format' : 'text',
            'api_key' : ''
        }
        
        response = json.loads(self.session.post(url=url, data=json.dumps(body)).text)
        return response['translatedText']