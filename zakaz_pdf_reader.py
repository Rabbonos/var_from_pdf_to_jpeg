from groq import Groq
import os
import pymupdf
from time import sleep
import json
from PIL import Image, ImageDraw, ImageFont
from narisovator import draw_second_table_row, draw_first_table

path_to_doc='test2.pdf'

doc = pymupdf.open(path_to_doc) # open a document
out = open("output.txt", "wb") # create a text output
for page in doc: # iterate the document pages
    text = page.get_text().encode("utf8") # get plain text (is in UTF-8)
    out.write(text) # write text of page
    out.write(bytes((12,))) # write page delimiter (form feed 0x0C)
out.close()

with open('output.txt', 'r', encoding='utf-8') as f:
    text=f.read()
#print(text)

def text_splitter(text):
    chunks=[text[ i*1500: 1500+1500*i] for i in range((len(text)//1500)+1) ]   
    return chunks

chunks=text_splitter(text)

GROQ_API_KEY = os.getenv("groqapi")

client = Groq(
    api_key=GROQ_API_KEY,
)
memory=[]
for chunk in chunks:
        sleep(2.5)
        chat_completion = client.chat.completions.create(
                messages=[
                    # Set an optional system message. This sets the behavior of the
                    # assistant and can be used to provide specific instructions for
                    # how it should behave throughout the conversation.
                    {
                        "role": "system",
                        "content": "you are an AI that parses small pieces of pdf files and tries to find what is asked of you.Answer in Russian only. Very short answers only."
                    },
                    # Set a user message for the assistant to respond to.
                    {
                        "role": "user",
                        "content": f'''Найди заказчика, найди адрес объекта контроля , найди производителя стеллажа (если неизвестен то найди предположение), найди высоту рамы (только цифры), профиль/сечение стойки(только цифры), длину каждой балки(только цифры), профиль/сечение каждой балки(только цифры) , найди максимально допустимые нагрузки на каждую пару балок(только цифры) и на весь стеллаж(только цифры). Формат твоего ответа только Json: заказчик:... , адрес объекта контроля:... , производитель стеллажа:... , комплектация(размеры):... , максимально допустимые нагрузки :... . 
                         Данные брать только из памяти и пдф кусочка и быть точным (комбинируй их). Если ничего не нашел то не пиши,  не делай своих предположений.Детали для понимания бери. память: {memory} , кусочек пдф: {chunk}''',
                    }
                ],
                model="llama3-70b-8192",
            )
        memory=chat_completion.choices[0].message.content
        print(chat_completion.choices[0].message.content)
#json checker
chat_completion = client.chat.completions.create(
                messages=[
                    # Set an optional system message. This sets the behavior of the
                    # assistant and can be used to provide specific instructions for
                    # how it should behave throughout the conversation.
                    {
                        "role": "system",
                        "content": "your task is to repair json if broken"
                    },
                    # Set a user message for the assistant to respond to.
                    {
                        "role": "user",
                        "content": f'''ANSWER IN JSON ONLY.DO NOT CHANGE DATA INSIDE. RENAME KEYS TO : 'заказчик', 'адрес объекта контроля','производитель стеллажа','комплектация(размеры)','высота рамы','профиль/сечение стойки','длина каждой балки','профиль/сечение каждой балки','максимально допустимые нагрузки','на каждую пару балок','на весь стеллаж'.Json to repair IF broken:{memory}''',
                    }
                ],
                model="llama3-70b-8192",
            )        
print('finallyyyyyyy')
json_data= json.loads(chat_completion.choices[0].message.content)
print(json_data)

# Load the image where you want to add the table row (optional, can create a blank image)
image_path = "outputzakaz.jpg"

image = Image.open(image_path)
# Initialize ImageDraw object
draw = ImageDraw.Draw(image)

draw_first_table(draw , json_data)
draw_second_table_row(draw, json_data)

image.save("output_with_table.jpg")
image.show()