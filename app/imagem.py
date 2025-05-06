import os
import requests
from app.database import Session, Imagem

def gerar_imagem(prompt, nome_arquivo):
    # ... código anterior ...
    with open(caminho, "wb") as f:
        f.write(imagem)
    # Salvar no banco de dados
    session = Session()
    nova_imagem = Imagem(nome_arquivo=nome_arquivo, prompt=prompt, caminho=caminho)
    session.add(nova_imagem)
    session.commit()
    session.close()
    return caminho
