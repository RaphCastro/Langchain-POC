import base64
import sys
import os
from dotenv import load_dotenv
import logging


def load_configurations(app):
    "Configuração geral das nossas variáveis de ambiente"
    load_dotenv()
    app.config["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    app.config["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")


def configure_logging():
    "Configuração basica para nossas logs"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stdout,
    )
