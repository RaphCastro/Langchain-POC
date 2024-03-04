import json
from langgraph.prebuilt import ToolInvocation
from langchain_core.messages import FunctionMessage
from app.chatbot.model import model
from app.chatbot.tools import tool_executor
from app.database.queries import select_all_sale_choices, update_step
from app.utils.products import get_product_info, get_products_by_category


def scan_first_message(state):
    prompt = f"Analise a mensagem: {state}, e classifique em um dos 4 tipos: saudacao, intencao de compra, confirmacao de compra, intencao de sair, duvida, responda somente com o tipo, sem nenhuma palavra a mais e sem acentuação"
    response = model.invoke(prompt)
    if response.content in ["saudacao", "intencao de compra", "intencao de sair", "duvida"]:
        response.content.replace("saudacao", "greet").replace("intencao de compra", "search_product").replace("confirmacao de compra", "confirm_purchase").replace("intencao de sair", "exit")
        update_step(response.content)
        return "continue"
    else:
        return "end"


def should_continue(state):
    messages = state["messages"]
    last_message = messages[-1]
    if "function_call" not in last_message.additional_kwargs:
        return "end"
    else:
        return "continue"


def call_model(state):
    messages = state["messages"]
    response = model.invoke(messages)
    print(f"RESPONSE: {response}\n MESSAGES: {messages}")
    return {"messages": [response]}


def call_tool(state):
    messages = state["messages"]
    last_message = messages[-1]
    print(last_message)
    action = ToolInvocation(
        tool=last_message.additional_kwargs["function_call"]["name"],
        tool_input=json.loads(
            last_message.additional_kwargs["function_call"]["arguments"]
        ),
    )
    response = tool_executor.invoke(action)
    function_message = FunctionMessage(content=str(response), name=action.tool)
    return {"messages": [function_message]}


def greet_user(state):
    greeting_message = "Você é uma loja virtual de roupas chamada CastroShop e deverá se apresentar como tal"
    greet_message = model.invoke(greeting_message)
    return {"messages": [greet_message]}


def search_product(state):
    try:
        messages = state["messages"]
        last_message = messages[-1]
        product_info = get_product_info(last_message)
        search_results = model.invoke(f"Informe ao cliente os produtos que encontrou, da seguinte forma: {product_info['nome']} - R${product_info['preco']:.2f} e pergunte se ele deseja comprar")
    except Exception as e:
        print(f"Erro ao obter informações do produto: {str(e)}")        
        product_info = get_products_by_category(last_message)
        search_results = model.invoke(f"Informe ao cliente os produtos que encontrou, da seguinte forma: {product_info['nome']} - R${product_info['preco']:.2f} e pergunte se ele deseja comprar")
    search_message = FunctionMessage(content=f"Resultados da busca: {', '.join(search_results)}", name="search_product")
    return {"messages": [search_message]}


def user_confirmation(state):
    prompt = f"Analise a mensagem: {state}, e classifique em um dos 2 tipos: aceita, recusa, responda somente com o tipo, sem nenhuma palavra a mais e sem acentuação"
    response = model.invoke(prompt)
    if response == "aceita":
        return "yes"
    else:
        return "no"


def confirm_purchase(state):
    messages = state["messages"]
    product = select_all_sale_choices()
    product_name = product[3]
    product_price = product[4]
    prompt = model.invoke(f"Você é uma loja e irá gerar uma confirmação de compra para o cliente, com preço e itens, aqui estão: {product_name}, {product_price}")
    return {"messages": [prompt]}


def send_negative(state):
    prompt = model.invoke(f"Você é uma loja virtual, e está lamentando pelo cliente não poder ter realizado a compra no momento, use a {state} como base histórica de mensagens")
    return {"messages": [prompt]}


def update_user_choice(state):
    messages = state["messages"]
