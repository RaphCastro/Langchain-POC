from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.utils.function_calling import convert_to_openai_function
from app.chatbot.tools import tools

load_dotenv()

model = ChatOpenAI(temperature=0, streaming=True)
functions = [convert_to_openai_function(t) for t in tools]
model = model.bind_functions(functions)
