import json
from pathlib import Path

DATA_DIR = Path(__file__).parent

with open(DATA_DIR / "orders.json") as f:
    ORDERS: list[dict] = json.load(f)

with open(DATA_DIR / "policies.json") as f:
    POLICIES: dict = json.load(f)

ORDERS_BY_ID: dict[str, dict] = {o["order_id"]: o for o in ORDERS}
