from langgraph.graph import StateGraph, END, Graph
from app.chatbot.agent_state import AgentState
from app.chatbot.functions import confirm_purchase, greet_user, scan_first_message, search_product, send_negative, user_confirmation
from app.database.queries import get_step
from app.utils.products import find_product_with_lowest_price


workflow = StateGraph(AgentState)


def retrieve_current_workflow():
    workflow.add_node("greet", greet_user)
    workflow.add_node("search_product", search_product)
    workflow.add_node("suggest_discounted_products", find_product_with_lowest_price)
    workflow.add_node("scan_answer", user_confirmation)
    workflow.add_node("confirm_purchase", confirm_purchase)
    workflow.add_node("negative_purchase", send_negative)
    workflow.add_node("scan_first_message", scan_first_message)
    workflow.set_entry_point("scan_first_message")
    workflow.add_conditional_edges("scan_first_message", scan_first_message, {"continue": get_step(1), "end": END})
    selector = get_step(1)
    workflow.add_edge("scan_first_message", selector)
    workflow.add_edge("greet", END)
    workflow.add_edge("suggest_discounted_products", END)
    workflow.add_edge("search_product", END)
    workflow.set_finish_point("search_product")
    workflow.add_conditional_edges("scan_answer", user_confirmation, {"yes": "confirm_purchase", "no":"negative_purchase"})
    workflow.add_edge("negative_purchase", END)
    workflow.set_finish_point("confirm_purchase")
    return workflow.compile()
