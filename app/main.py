from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.imagem import gerar_imagem

app = FastAPI()

class RequisicaoImagem(BaseModel):
    prompt: str
    nome_arquivo: str

@app.post("/gerar-imagem")
def gerar_imagem_endpoint(requisicao: RequisicaoImagem):
    try:
        caminho = gerar_imagem(requisicao.prompt, requisicao.nome_arquivo)
        return {"mensagem": "Imagem gerada com sucesso!", "caminho": caminho}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
