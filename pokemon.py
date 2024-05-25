import requests
from bs4 import BeautifulSoup
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A3
from reportlab.lib.units import mm
from PIL import Image
import math
import asyncio
import glob

# ポケモンカード
class PokemonCard:
    file_path = ""
    csv_file_name = ""
    splited_pdf_name_int = 0
    card_title_list = []
    card_name = ""
    decki_name = ""

    def __init__(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.transaction())

    # 一連の処理
    async def transaction(self):
        await self.deleteFiles()
        await self.readFile()
        await self.saveImage()
        await self.savePdf()

    # 画像ファイルを削除
    async def deleteFiles(self):
        self.deleteFilesWithDirectory("/imagedata/*")
        self.deleteFilesWithDirectory("/save/*")
        self.deleteFilesWithDirectory("/sample/pokemon/*")
    
    # 画像ファイルを削除
    def deleteFilesWithDirectory(self, file_name):
        dire = os.getcwd() + file_name
        files = glob.glob(dire)
        for file in files:
            os.remove(file)

    # ポケモンのCSVファイルを読み込み
    async def readFile(self):
        csv_dir = os.getcwd() + "/sample_csv"
        self.csv_file_name = 'pokemon.csv'
        self.file_path = os.path.join(csv_dir, self.csv_file_name)
        with open(self.file_path, encoding = 'utf-8') as f:
            lines = f.readlines()
        self.card_title_list = [ line.strip() for line in lines]
        # CSVファイルの先頭の文字列をファイル名称に設定
        self.decki_name = self.card_title_list[0]
        # CSVファイルのコメントを読み込まない
        self.card_title_list = [i for i in self.card_title_list if i.find('#') < 0]
        # CSVファイルの改行を読み込まない
        self.card_title_list = [i for i in self.card_title_list if i != ""]

    # 画像を保存
    async def saveImage(self):
        for card_title in self.card_title_list:
            print(card_title)
            headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0",
            }
            target_url = "https://www.pokemon-card.com/card-search/details.php/card/" + card_title + "/regu/all"
            r = requests.get(target_url,headers=headers)
            soup = BeautifulSoup(r.text,"html.parser")
            elems = soup.select("img")
            h1 = soup.find_all('h1')
            for value in h1:
                text = value.text.strip()
                self.card_name = text
            for elem in elems:
                baseUrl = "https://www.pokemon-card.com/"
                src = elem.get("src")
                root_ext_pair = os.path.splitext(src)
                extention = root_ext_pair[-1]
                if extention == ".jpg":
                    baseUrl = baseUrl +  src
                    r = requests.get(baseUrl)
                    image_path = './imagedata/' + card_title + '.jpg'
                    image_file = open(image_path, 'wb')
                    image_file.write(r.content)
                    image_file.close()
                    image = Image.open(image_path)
                    save_path = './save/' + card_title + '.jpg'
                    os.makedirs(os.path.dirname(save_path), exist_ok=True)
                    if self.card_name.find('BREAK') > 0:
                        image.save(save_path)
                    else:
                        rotated_image = image.rotate(90, expand=True)
                        rotated_image.save(save_path)

    # PDFを保存
    async def savePdf(self):
        i = 0
        j = 0
        x = 0
        pages = math.ceil(len(self.card_title_list) / 4)
        splited_csv_file_name = self.csv_file_name.split(".")
        for p in range(pages):
            p = p + self.splited_pdf_name_int
            pdf_path = "./sample/" + splited_csv_file_name[0] + "/" + splited_csv_file_name[0] + "_" + self.decki_name + "_" + str(p) + ".pdf"
            os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
            pdf = canvas.Canvas(pdf_path, pagesize=landscape(A3))
            for j in range(4):
                if x == len(self.card_title_list):
                    break
                select_card_title = self.card_title_list[x]
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

pokemonCard = PokemonCard()