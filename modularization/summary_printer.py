"""Modul untuk mencetak ringkasan ke layar."""


def print_summary(total_orders: int, grand_total: float) -> None:
    """Cetak ringkasan ke layar."""
    print(f"Total orders : {total_orders}")
    print(f"Grand total  : {grand_total:.2f}")