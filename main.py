import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

import os
import io
import base64
import random
import requests
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image, ImageEnhance
import replicate

app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuração das variáveis de ambiente
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
STABLE_DIFFUSION_API_KEY = os.getenv("STABLE_DIFFUSION_API_KEY")
STABLE_DIFFUSION_URL = "https://api.stability.ai/v1/generate"  # Substitua pelo URL correto da API

# Inicialização do cliente Replicate
replicate_client = replicate.Client(api_token=REPLICATE_API_TOKEN)

# Tags para as plataformas
tags_instagram = ["#instafood", "#foodie", "#delicious", "#homemade", "#comidaboa"]
tags_tiktok = ["#foodtok", "#receita", "#dicas", "#culinaria", "#viral"]

# Modelos de dados
class TextoInput(BaseModel):
    produto: str
    plataforma: str

class Agendamento(BaseModel):
    horario: str
    plataforma: str
    conteudo: str

# Lista para armazenar agendamentos
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
    plataforma = dados.plataforma.lower()
    if plataforma == "instagram":
        tags = tags_instagram
    elif plataforma == "tiktok":
        tags = tags_tiktok
    else:
        tags = ["#Essentia"]
    descricao = f"Descubra o sabor incrível do {dados.produto}! Ideal para quem ama {plataforma}. {' '.join(tags)}"
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
        headers = {
            "Authorization": f"Bearer {STABLE_DIFFUSION_API_KEY}",
            "Content-Type": "application/json"
        }
        response = requests.post(STABLE_DIFFUSION_URL, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Erro na requisição: {str(e)}")
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

# Inicialização do servidor
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
