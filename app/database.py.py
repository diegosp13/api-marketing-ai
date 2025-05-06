from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

engine = create_engine("sqlite:///data/imagens.db")
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Imagem(Base):
    __tablename__ = "imagens"
    id = Column(Integer, primary_key=True)
    nome_arquivo = Column(String)
    prompt = Column(String)
    caminho = Column(String)
    data_criacao = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(engine)
