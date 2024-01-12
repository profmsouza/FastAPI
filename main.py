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
async def create_sticker(u: str, b: str, m: str, y:str, a: str, c: str, n: str, e1: str, e2: str, e3: str, e4: str):
    image = Image.open("i.png")
    q = make_q(u)
    response = requests.get(q)
    qr = Image.open(io.BytesIO(response.content))
    width, height = qr.size
    new_width = round(width * 6)
    new_height = round(height * 6)
    qr = qr.resize((new_width, new_height))
    image.paste(qr, (47,260))
    draw = ImageDraw.Draw(image)
    h,v,s=[10,15,40]
    draw.text((35, 10), b, font=load_font(100), fill=(255,255,0))
    draw.text((35, 100), m, font=load_font(60), fill=(255,255,0))
    draw.text((260, 150), str(int(y)), font=load_font(80), fill=(255,255,0))
    draw.text((240, 1295), u, font=load_font(80), fill=(255,255,0))
    draw.text((1180, 1380), c, font=load_font(30), fill=(72,72,72))
    draw.text((1145, 1530), c, font=load_font(30), fill=(72,72,72))
    draw.text((150+h, 1570+v+0*s), n, font=load_font(60), fill=(0,0,0))
    draw.text((150+h, 1570+v+2*s), e1, font=load_font(50), fill=(0,0,0))
    draw.text((150+h, 1570+v+3*s), e2, font=load_font(50), fill=(0,0,0))
    draw.text((150+h, 1570+v+4*s), e3, font=load_font(50), fill=(0,0,0))
    draw.text((150+h, 1570+v+5*s), e4, font=load_font(50), fill=(0,0,0))
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
