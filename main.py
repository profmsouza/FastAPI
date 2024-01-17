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
    draw.text((260, 150), y, font=load_font(80), fill=(255,255,0))
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
    draw.text((800, 1220), a, font=load_font(110), fill=(255,255,0))
    image = image.rotate(90, expand=True)
    image.save("is.png")
    image_crop = image.crop((0, 0, 1414, 1433))
    image_crop.save("is_c.png")
    client_id = os.environ.get('CLIENT_ID')
    im = pyimgur.Imgur(client_id)
    filename = 'is.png'
    up_img = im.upload_image(filename, title="ys")
    up_img_c = im.upload_image('is_c.png', title="ys_c")
    return {"link": up_img.link, "link_c": up_img_c.link}

#https://fastapi-production-0266.up.railway.app/sticker?u=https://tinyurl.com/29564pct&b=HITECH%20ELECTRIC&m=MODELO&y=2021&a=ESSE%20CARRO%20LEGAL&c=H1992023175615H&n=UM%20DOIS%20TR%C3%8AS%20DA%20SILVA%20QUATRO&e1=Rua%20A,%20486%20-%20Casa&e2=BAIRRO%20LEGAL&e3=Governador%20Valadares&e4=CEP%2035065-000
