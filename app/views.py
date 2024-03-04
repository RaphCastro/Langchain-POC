from flask import Blueprint, jsonify, request
from langchain_core.messages import HumanMessage
from app.chatbot.graph import retrieve_current_workflow
from app.database.queries import get_step, insert_conversation

api_blueprint = Blueprint("API", __name__)


@api_blueprint.route("/message", methods=["GET"])
def message():
    selector = get_step(1)
    if selector is None:
        insert_conversation()
    request_data = request.get_json()
    user_id = request_data.get("id")
    message = request_data.get("message")
    if user_id is None or message is None:
        return jsonify({"Status": "Error", "Message": "Missing 'user_id' or 'message' in the request JSON"}), 400
    inputs = {"messages": [HumanMessage(content="Aceito a compra")]}
    retriever = retrieve_current_workflow()
    invoker = retriever.invoke(inputs)
    return jsonify({"AIMessage": invoker, "HumanMessage": inputs}, 200)
