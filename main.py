from fastapi import FastAPI, HTTPException
import uvicorn
from PIL import Image, ImageDraw, ImageFont
import pyimgur
import requests
import io

app = FastAPI()

@app.get("/")
async def hello():
  return {"Welcome": "iSell API is online"}

@app.get("/sticker")
async def create_sticker(url: str, brand: str, model: str, year:str, adj: str, code: str, nome: str, end1: str, end2: str, end3: str, end4: str):
    # Imagem base
    image = Image.open("iSell Sticker.png")

    # QRCODE
    qr_link="https://quickchart.io/qr?text=" + url + "&light=ffffff00&dark=ffff00"
    response = requests.get(qr_link)
    qr = Image.open(io.BytesIO(response.content))
    k = 6
    cor = (255,255,0)
    width, height = qr.size
    new_width = round(width * k)
    new_height = round(height * k)
    qr = qr.resize((new_width, new_height))

    # Composição
    image.paste(qr, (47,260))
    draw = ImageDraw.Draw(image)
    font200 = ImageFont.truetype("BebasNeue-Regular.ttf", 200)
    font180 = ImageFont.truetype("BebasNeue-Regular.ttf", 180)
    font140 = ImageFont.truetype("BebasNeue-Regular.ttf", 140)
    font120 = ImageFont.truetype("BebasNeue-Regular.ttf", 120)
    font110 = ImageFont.truetype("BebasNeue-Regular.ttf", 110)
    font100 = ImageFont.truetype("BebasNeue-Regular.ttf", 100)
    font80 = ImageFont.truetype("BebasNeue-Regular.ttf", 80)
    font60 = ImageFont.truetype("BebasNeue-Regular.ttf", 60)
    font50 = ImageFont.truetype("BebasNeue-Regular.ttf", 50)
    font40 = ImageFont.truetype("BebasNeue-Regular.ttf", 40)
    font30 = ImageFont.truetype("BebasNeue-Regular.ttf", 30)
    font20 = ImageFont.truetype("BebasNeue-Regular.ttf", 20)
    draw.text((35, 10), brand, font=font100, fill=cor)
    draw.text((35, 100), model, font=font60, fill=cor)
    draw.text((260, 150), year, font=font80, fill=cor)
    draw.text((240, 1295), url, font=font80, fill=cor)
    draw.text((1180, 1380), code, font=font30, fill=(72,72,72))
    draw.text((1145, 1530), code, font=font30, fill=(72,72,72))

    h=10
    v=15
    s=40
    draw.text((150+h, 1570+v+0*s), nome, font=font60, fill=(0,0,0))
    draw.text((150+h, 1570+v+2*s), end1, font=font50, fill=(0,0,0))
    draw.text((150+h, 1570+v+3*s), end2, font=font50, fill=(0,0,0))
    draw.text((150+h, 1570+v+4*s), end3, font=font50, fill=(0,0,0))
    draw.text((150+h, 1570+v+5*s), end4, font=font50, fill=(0,0,0))

    image = image.rotate(-90, expand=True)
    draw = ImageDraw.Draw(image)
    draw.text((800, 1220), "ESSE CARRO " + adj, font=font110, fill=cor)
    image = image.rotate(90, expand=True)


    # Salvando composição
    image.save("iSellCode.png")

    # Upload
    client_id = 'cf3f05cef69c138'
    im = pyimgur.Imgur(client_id)
    filename = 'iSellCode.png'
    up_img = im.upload_image(filename, title="Seu adesivo")

    # Retornando o link direto para a imagem
    return {"link": up_img.link}

#http://127.0.0.1:8000/sticker?url=https://tinyurl.com/29564pct&brand=RENAULT&model=DUSTER&year=2021&adj=MARAVIHOSO&code=H1992023175615H&nome=MÁRCIO LUÍS MOREIRA DE SOUZA&end1=Rua L, 486 - Casa&end2=Parque Olímpico&end3=Governador Valadares&end4=CEP 35065-242
