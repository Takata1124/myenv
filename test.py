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

directory = './sample'  # ファイル名を取得したいディレクトリのパス
file_names = os.listdir(directory)
splited_pdf_name_int = 0
csv_dir = os.getcwd() + "/sample_csv"
csv_file_name = 'yami.csv'
file_path = os.path.join(csv_dir, csv_file_name)

with open(file_path, encoding = 'utf-8') as f:
    lines = f.readlines()
card_title_list = [ line.strip() for line in lines]

for card_title in card_title_list:
    s_quote_url = urllib.parse.quote(card_title)
    prefix_url = 'https://torekakaku.com/dm/search/?q='
    suffix_url = '&k=&from=all&to=all&z=0&bunrui=0&d=0&order=&d=0'
    total_url = prefix_url + s_quote_url + suffix_url
    response = requests.get(total_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all("img")
    img_urls = []

    for img_tag in img_tags:
        url = img_tag.get("src")
        if url != None and 'https://torekakaku.com/dm/image/' in url and len(img_urls) < 1:
            img_urls.append(url)

    i = 0
    for image_data in img_urls:
        r = requests.get(image_data)
        image_path = './imagedata/' + card_title + '.jpg'
        image_file = open(image_path, 'wb')
        image_file.write(r.content)
        image_file.close()
        image = Image.open(image_path)
        rotated_image = image.rotate(90, expand=True)
        save_path = './save/' + card_title + '.jpg'
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        rotated_image.save(save_path)
        i += 1
    
pages = math.ceil(len(card_title_list) / 4)

i = 0
j = 0
x = 0

splited_csv_file_name = csv_file_name.split(".")

for p in range(pages):
    p = p + splited_pdf_name_int
    print(p)
    p_str = str(p)
    pdf_path = "./sample/" + splited_csv_file_name[0] + "/" + splited_csv_file_name[0] + "_" + p_str + ".pdf"
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    pdf = canvas.Canvas(pdf_path, pagesize=landscape(A3))
    for j in range(4):
        if x == len(card_title_list):
            break
        select_card_title = card_title_list[x]
        for i in range(4):
            dx = 0*mm + 88*mm * i
            dy = 0*mm + 63*mm * j
            dWidth = 88*mm
            dHeight = 63*mm
            prefix_card_path = "./save/"
            suffix_card_path = ".jpg"
            total_card_path = prefix_card_path + select_card_title + suffix_card_path
            pdf.drawImage(total_card_path, dx, dy, dWidth, dHeight)
        x += 1
    pdf.save()  