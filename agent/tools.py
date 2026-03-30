from datetime import date, timedelta
from langchain_core.tools import tool
from data.data_store import ORDERS_BY_ID


@tool
def lookup_order(order_id: str) -> str:
    """Look up an order by its order ID. Returns order details or a not-found message."""
    order = ORDERS_BY_ID.get(order_id)
    if not order:
        return f"No order found with ID '{order_id}'."
    return str(order)


@tool
def check_return_eligibility(order_id: str) -> str:
    """Check if an order is eligible for return based on delivery date and return window."""
    order = ORDERS_BY_ID.get(order_id)
    if not order:
        return f"No order found with ID '{order_id}'."
    if order["status"] != "delivered":
        return f"Order {order_id} is not delivered yet (status: {order['status']}). Returns only apply to delivered orders."
    delivery_date = date.fromisoformat(order["delivery_date"])
    window = order.get("return_window_days", 7)
    deadline = delivery_date + timedelta(days=window)
    days_remaining = (deadline - date.today()).days
    if days_remaining >= 0:
        return f"Order {order_id} ({order['item']}) IS eligible for return. {days_remaining} day(s) remaining in the return window (deadline: {deadline})."
    return f"Order {order_id} ({order['item']}) is NOT eligible for return. The return window expired {abs(days_remaining)} day(s) ago (deadline was {deadline})."
