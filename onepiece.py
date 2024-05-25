import requests
from bs4 import BeautifulSoup
import urllib.parse
import os
import csv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A3
from reportlab.lib.units import mm
from PIL import Image
import math

class SimpleData:

    file_path = ""
    csv_file_name = ""
    splited_pdf_name_int = 0

    def __init__(self):
        self.readFile()
        self.make()

    def readFile(self):
        csv_dir = os.getcwd() + "/sample_csv"
        self.csv_file_name = 'yami.csv'
        self.file_path = os.path.join(csv_dir, self.csv_file_name)

    def make(self):
        headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0",
        }
        target_url = "https://www.onepiece-cardgame.com/cardlist/#group_1-1"
        r = requests.get(target_url,headers=headers)
        print(r)
        soup = BeautifulSoup(r.text,"html.parser")
        elems = soup.select("img")
        list = []
        
        for elem in elems:
            #src属性を取得(文字列型)
            baseUrl = "https://www.onepiece-cardgame.com"
            src = elem.get("src")
            print(src)
            # src = src.split('/')
            # del src[0]
            # for index, item in enumerate(src):
            #     baseUrl = baseUrl + "/" + item
            #     if index == len(src) - 1:
            #         list.append(baseUrl)

        # i = 0
        # for imageUrl in list:
        #     print(imageUrl)
        #     if imageUrl.find('ico') > 0:
        #         pass
        #     elif imageUrl.find('logo') > 0:
        #         pass
        #     else:
        #         r = requests.get(imageUrl)
        #         image_path = './imagedata/' + str(i) + '.png'
        #         image_file = open(image_path, 'wb')
        #         image_file.write(r.content)
        #         image_file.close()
        #         image = Image.open(image_path)
        #         rotated_image = image.rotate(90, expand=True)
        #         save_path = './save/' + str(i) + '.png'
        #         os.makedirs(os.path.dirname(save_path), exist_ok=True)
        #         rotated_image.save(save_path)
        #         i += 1
            
        # pages = math.ceil(len(list) / 4)

        # i = 0
        # j = 0
        # x = 0

        # for p in range(pages):
        #     p = p + self.splited_pdf_name_int
        #     p_str = str(p)
        #     pdf_path = "./sample/" + p_str + ".pdf"
        #     os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
        #     pdf = canvas.Canvas(pdf_path, pagesize=landscape(A3))
        #     for j in range(4):
        #         if x == len(list):
        #             break
        #         # select_card_title = list[x]
        #         for i in range(4):
        #             dx = 0*mm + 88*mm * i
        #             dy = 0*mm + 63*mm * j
        #             dWidth = 88*mm
        #             dHeight = 63*mm
        #             prefix_card_path = "./save/"
        #             suffix_card_path = ".png"
        #             total_card_path = prefix_card_path + str(x) + suffix_card_path
        #             pdf.drawImage(total_card_path, dx, dy, dWidth, dHeight)
        #         x += 1
        #     pdf.save() 

data1 = SimpleData()