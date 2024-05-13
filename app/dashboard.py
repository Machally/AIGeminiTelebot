from flask import request, Response
from app import app
import requests
from dotenv import load_dotenv
from os import environ
import google.generativeai as genai
import os
from dotenv import load_dotenv
import re
import json 
from PIL import Image
import fitz

load_dotenv()
bot_token = environ.get("bot_token")
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
model = genai.GenerativeModel('gemini-1.5-pro-latest')
chat = model.start_chat(history=[])

def get_document(pdf_file_path):
    doc = fitz.open(pdf_file_path)
    page_num = doc.page_count
    output = []
    for i in range(page_num):
        page = doc.load_page(i)  # number of page
        pix = page.get_pixmap()
        output.append("./outfile{}.png".format(i))
        pix.save(output[i])
    doc.close()
    return output

@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        return "<h1>Gemini Bot Aplication is running!</h1>"
    
@app.route('/', methods=['POST'])
def post_example():
    if request.method == 'POST':
        # Access POST data from the request
        msg = request.get_json()   

        chat_id = msg['message']['chat']['id']
        try:
            text = msg['message']['text'] # This gets the text from the msg
            response = chat.send_message(text)
            url = f'https://api.telegram.org/bot{bot_token}/sendMessage?parse_mode=markdown' # Calling the telegram API to reply the message
            
            payload = {
                'chat_id': chat_id,
                'text': response.text
            }
            r = requests.post(url, json=payload)
            if r.status_code == 200:
                return Response('ok', status=200)
            else: 
                return Response('Failed to send message to Telegram', status=500)
        except:
            try:
                file_id = msg['message']['photo'][2]['file_id']
                text = msg['message']['caption']                    
                url = f"https://api.telegram.org/bot{bot_token}/getFile?file_id={file_id}"
                r = requests.post(url, json=[])
                data = r.json()
                file_path = data['result']['file_path']
                url = f"https://api.telegram.org/file/bot{bot_token}/{file_path}"
            
                response = requests.get(url)
                
                if response.status_code == 200:
                    with open('./' + file_path, 'wb') as file:
                        file.write(response.content)
                image = Image.open(file_path)
                
                response = chat.send_message([text, image])
                url = f'https://api.telegram.org/bot{bot_token}/sendMessage?parse_mode=markdown' # Calling the telegram API to reply the message
            
                payload = {
                    'chat_id': chat_id,
                    'text': response.text
                }
                r = requests.post(url, json=payload)
                os.remove(file_path)
                if r.status_code == 200:
                    return Response('ok', status=200)
                else: 
                    return Response('Failed to send message to Telegram', status=500)
                
            except:
                try:
                    file_id = msg['message']['document']['file_id']
                    text = msg['message']['caption']   
                    url = f"https://api.telegram.org/bot{bot_token}/getFile?file_id={file_id}"
                    r = requests.post(url, json=[])
                    data = r.json()
                    file_path = data['result']['file_path']
                    url = f"https://api.telegram.org/file/bot{bot_token}/{file_path}" 
                    response = requests.get(url)

                    if response.status_code == 200:
                        with open('./' + file_path, 'wb') as file:
                            file.write(response.content)
                    pdf_obj = get_document(file_path)
                    os.remove(file_path)
                    files = []
                    for p in range(len(pdf_obj)):
                        files.append(genai.upload_file(path=pdf_obj[p]))
                    response = chat.send_message([text] + files)
                    for arquivo in pdf_obj:
                        os.remove(arquivo)
                    url = f'https://api.telegram.org/bot{bot_token}/sendMessage?parse_mode=markdown' # Calling the telegram API to reply the message
            
                    payload = {
                        'chat_id': chat_id,
                        'text': response.text
                    }
                    r = requests.post(url, json=payload)
                    if r.status_code == 200:
                        return Response('ok', status=200)
                    else: 
                        return Response('Failed to send message to Telegram', status=500)
                except:
                    try:
                        file_id = msg['message']['audio']['file_id']
                        text = msg['message']['caption']
                        url = f"https://api.telegram.org/bot{bot_token}/getFile?file_id={file_id}"
                        r = requests.post(url, json=[])
                        data = r.json()
                        file_path = data['result']['file_path']
                        url = f"https://api.telegram.org/file/bot{bot_token}/{file_path}" 
                        response = requests.get(url)

                        if response.status_code == 200:
                            with open('./' + file_path, 'wb') as file:
                                file.write(response.content) 
                        audio_file = genai.upload_file('./' + file_path)          
                        response = chat.send_message([text, audio_file])
                        url = f'https://api.telegram.org/bot{bot_token}/sendMessage' # Calling the telegram API to reply the message
            
                        payload = {
                            'chat_id': chat_id,
                            'text': response.text
                        }
                        r = requests.post(url, json=payload)
                        os.remove(file_path)
                        if r.status_code == 200:
                            return Response('ok', status=200)
                        else: 
                            return Response('Failed to send message to Telegram', status=500)
                            
                    except Exception as inst:
                        print(inst)
                        print('Error: Invalid Message')
                        url = f'https://api.telegram.org/bot{bot_token}/sendMessage?parse_mode=markdown' # Calling the telegram API to reply the message
            
                        payload = {
                            'chat_id': chat_id,
                            'text': 'Algo inesperado ocorreu... *Tente novamente*.'
                        }
                        r = requests.post(url, json=payload)
                        if r.status_code == 200:
                            return Response('ok', status=200)
                        else: 
                            return Response('Failed to send message to Telegram', status=500)
            
    return Response('ok', status=200)
 
if __name__ == '__main__':
   app.run(debug=True)

