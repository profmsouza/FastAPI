from fastapi import FastAPI, HTTPException
import hypercorn
from PIL import Image, ImageDraw
import pyimgur
import requests
import io
import os
from add import make_q, load_font

app = FastAPI()

@app.get("/")
async def hello():
  return {"Welcome": "It is online!"}

@app.get("/sticker")
async def create_sticker(url: str, brand: str, model: str, year:str, adj: str, code: str, nome: str, end1: str, end2: str, end3: str, end4: str):
    image = Image.open("i.png")
    q = make_q(url)
    response = requests.get(q)
    qr = Image.open(io.BytesIO(response.content))
    width, height = qr.size
    new_width = round(width * 6)
    new_height = round(height * 6)
    qr = qr.resize((new_width, new_height))
    image.paste(qr, (47,260))
    draw = ImageDraw.Draw(image)
    h,v,s=[10,15,40]
    draw.text((35, 10), brand, font=load_font(100), fill=(255,255,0))
    draw.text((35, 100), model, font=load_font(60), fill=(255,255,0))
    draw.text((260, 150), str(int(year)), font=load_font(80), fill=(255,255,0))
    draw.text((240, 1295), url, font=load_font(80), fill=(255,255,0))
    draw.text((1180, 1380), code, font=load_font(30), fill=(72,72,72))
    draw.text((1145, 1530), code, font=load_font(30), fill=(72,72,72))
    draw.text((150+h, 1570+v+0*s), nome, font=load_font(60), fill=(0,0,0))
    draw.text((150+h, 1570+v+2*s), end1, font=load_font(50), fill=(0,0,0))
    draw.text((150+h, 1570+v+3*s), end2, font=load_font(50), fill=(0,0,0))
    draw.text((150+h, 1570+v+4*s), end3, font=load_font(50), fill=(0,0,0))
    draw.text((150+h, 1570+v+5*s), end4, font=load_font(50), fill=(0,0,0))
    image = image.rotate(-90, expand=True)
    draw = ImageDraw.Draw(image)
    draw.text((800, 1220), adj, font=load_font(110), fill=(255,255,0))
    image = image.rotate(90, expand=True)
    image.save("is.png")
    client_id = os.environ.get('CLIENT_ID')
    im = pyimgur.Imgur(client_id)
    filename = 'is.png'
    up_img = im.upload_image(filename, title="ys")
    return {"link": up_img.link}
