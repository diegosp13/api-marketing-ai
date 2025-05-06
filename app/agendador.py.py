from apscheduler.schedulers.background import BackgroundScheduler
from app.redes_sociais import postar_imagem

def agendar_postagem(caminho_imagem, texto, data_hora):
    scheduler = BackgroundScheduler()
    scheduler.add_job(postar_imagem, 'date', run_date=data_hora, args=[caminho_imagem, texto])
    scheduler.start()
