"""Modul untuk membaca orders dari file CSV."""
import csv


def read_orders(file_path: str) -> list[dict]:
    """Membaca orders.csv dan mengembalikan list of dict."""
    orders = []
    with open(file_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            orders.append({
                "item": row["item"],
                "price": float(row["price"]),
                "quantity": int(row["quantity"]),
                "is_member": row["is_member"].lower() == "true",
            })
    return orders