from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image, ImageEnhance
import io
import base64
import requests
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

tags_instagram = ["#instafood", "#foodie", "#delicious", "#homemade", "#comidaboa"]
tags_tiktok = ["#foodtok", "#receita", "#dicas", "#culinaria", "#viral"]

class TextoInput(BaseModel):
    produto: str
    plataforma: str

class Agendamento(BaseModel):
    horario: str
    plataforma: str
    conteudo: str

agendamentos = []

@app.post("/melhorar-imagem")
async def melhorar_imagem(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes))
        enhanced = ImageEnhance.Color(image).enhance(1.6)
        enhanced = ImageEnhance.Sharpness(enhanced).enhance(2.0)
        buf = io.BytesIO()
        enhanced.save(buf, format="PNG")
        base64_image = base64.b64encode(buf.getvalue()).decode("utf-8")
        return {"status": "ok", "imagem_base64": base64_image}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/gerar-descricao")
def gerar_descricao(dados: TextoInput):
    if dados.plataforma.lower() == "instagram":
        tags = tags_instagram
    elif dados.plataforma.lower() == "tiktok":
        tags = tags_tiktok
    else:
        tags = ["#Essentia"]
    descricao = f"Descubra o sabor incrível do {dados.produto}! Ideal para quem ama {dados.plataforma}. {' '.join(tags)}"
    return {"descricao": descricao, "tags": tags}

@app.post("/variar-imagem")
async def variar_imagem(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        img_base64 = base64.b64encode(image_bytes).decode("utf-8")
        payload = {
            "init_images": [img_base64],
            "prompt": "foto criativa e atrativa de comida para marketing",
            "steps": 20
        }
        # 🔴 Substitua este endpoint por um válido da sua API do Stable Diffusion
        response = requests.post("https://api.exemplo-stable-diffusion.com/sdapi/v1/img2img", json=payload)
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/agendar-post")
def agendar_post(data: Agendamento):
    agendamentos.append({
        "horario": data.horario,
        "plataforma": data.plataforma,
        "conteudo": data.conteudo
    })
    return {"status": "agendado", "total_agendados": len(agendamentos)}

@app.get("/melhor-horario")
def melhor_horario():
    horarios = ["11:00", "13:00", "18:00", "20:00"]
    escolhido = random.choice(horarios)
    return {"melhor_horario": escolhido}

@app.post("/upload-simulado")
def upload_simulado(dados: TextoInput):
    return {
        "status": "enviado",
        "plataforma": dados.plataforma,
        "mensagem": f"Postagem simulada em {dados.plataforma} com o produto {dados.produto}"
    }

@app.get("/agendamentos")
def listar_agendamentos():
    return {"agendamentos": agendamentos}
