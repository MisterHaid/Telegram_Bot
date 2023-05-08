import random
import sqlite3
import requests
from bs4 import BeautifulSoup
from time import sleep
import telebot
from telebot import types
API_KEY="5930673731:AAHYgQjAdc3U_9aDd8qBSGUxqBEpsuHmagg"
index=0

class Product:
    def __init__(self,name, price, image):
        self.name=name
        self.price=price
        self.image=image
    def getname(self):
        return self.name
    def getprice(self):
        return self.price
    def getimage(self):
        return self.image

def parser(URL):
    SavedProduct=[]

    for count in range(1,2):
        response= requests.get(URL)
        soup=BeautifulSoup(response.text,"lxml")
        data=soup.find_all("div",class_="product-card-wrapper")
        for i in data:
            name = i.find("div", class_="product-card-title__wrapper").text
            url_image = i.find("img", class_="product-card__image").get("src")
            price_new = i.find("div", class_="price-new").text
            product= Product(name,price_new,url_image)
            SavedProduct.append(product)
    return SavedProduct


bot=telebot.TeleBot(API_KEY)
url1="https://www.perekrestok.ru/cat/d/122/syr"
url2="https://www.perekrestok.ru/cat/d/114/moloko"
url3="https://www.perekrestok.ru/cat/d/118/smetana"
url4="https://www.perekrestok.ru/cat/d/153/frukty"
url5="https://www.perekrestok.ru/cat/d/656/syrki"
url6="https://www.perekrestok.ru/cat/d/133/kolbasa"
url7="https://www.perekrestok.ru/cat/d/209/gazirovannye-napitki"


def into_base(index,lists):
    base_product=[]
    base_name = []
    base_price = []
    for i in lists:
        name, price = i.getname(),i.getprice()
        base_name.append(str(name))
        base_price.append(str(price))
    for i in range(len(base_name)):
        index+=1
        cur.execute("INSERT INTO base VALUES(?, ?, ?);", (f'{index}',f'{base_name[i]}',f'{base_price[i]}'))
        conn.commit()
    return index


conn= sqlite3.connect('database.db')
cur= conn.cursor()
data="""CREATE TABLE IF NOT EXISTS base(ID INTEGER,name TEXT,price TEXT) """
cur.execute(data)
conn.commit()


listsale1 = parser(url1)
listsale2 = parser(url2)
listsale3 = parser(url3)
listsale4 = parser(url4)
listsale5 = parser(url5)
listsale6 = parser(url6)
listsale7 = parser(url7)
index=into_base(index,listsale1)
index=into_base(index,listsale2)
index=into_base(index,listsale3)
index=into_base(index,listsale4)
index=into_base(index,listsale5)
index=into_base(index,listsale6)
index=into_base(index,listsale7)






@bot.message_handler(commands=['start'])
def start(message):
    markup= types.ReplyKeyboardMarkup(resize_keyboard=True)
    item2 = types.KeyboardButton('Молоко')
    item3 = types.KeyboardButton('Сыр')
    item4 = types.KeyboardButton('Сырки')
    item5 = types.KeyboardButton('Сметана')
    item6 = types.KeyboardButton('Фрукты')
    item7 = types.KeyboardButton('Газированные напитки')
    item8 = types.KeyboardButton('Колбаса')

    markup.add(item2,item3,item4,item5,item6,item7,item8)

    bot.send_message(message.chat.id,f"Здравствуйте , {message.from_user.first_name}! На какие продукты хотите получить акции?".format(message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def sales(message):
    if message.chat.type== 'private':
        if message.text=='Молоко':
            i=random.randint(0,len(listsale2)-1)
            bot.send_message(message.chat.id,listsale2[i].getname()+'\n'+listsale2[i].getprice()+'\n'+ listsale2[i].getimage())
        elif message.text == 'Сыр':
            i = random.randint(0, len(listsale1)-1)
            bot.send_message(message.chat.id, listsale1[i].getname()+'\n'+listsale1[i].getprice()+'\n'+listsale1[i].getimage())

        elif message.text == 'Сметана':
            i = random.randint(0, len(listsale3)-1)
            bot.send_message(message.chat.id, listsale3[i].getname()+'\n'+listsale3[i].getprice()+'\n'+listsale3[i].getimage())

        elif message.text == 'Газированные напитки':
            i = random.randint(0, len(listsale7)-1)
            bot.send_message(message.chat.id,listsale7[i].getname() +'\n'+ listsale7[i].getprice() +'\n'+ listsale7[i].getimage())
        elif message.text == 'Колбаса':
            i = random.randint(0, len(listsale6)-1)
            bot.send_message(message.chat.id,listsale6[i].getname() +'\n'+ listsale6[i].getprice() +'\n'+ listsale6[i].getimage())
        elif message.text == 'Сырки':
            i = random.randint(0, len(listsale5)-1)
            bot.send_message(message.chat.id,listsale5[i].getname() +'\n'+ listsale5[i].getprice() +'\n'+ listsale5[i].getimage())
        elif message.text == 'Фрукты':
            i = random.randint(0, len(listsale4)-1)
            bot.send_message(message.chat.id, listsale4[i].getname()+'\n'+listsale4[i].getprice()+'\n'+listsale4[i].getimage())





bot.polling()
