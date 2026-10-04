"""Modul untuk menghitung subtotal, diskon, dan pajak."""

MEMBER_DISCOUNT_RATE = 0.10
TAX_RATE = 0.11


def calculate_subtotal(price: float, quantity: int) -> float:
    return price * quantity


def apply_member_discount(subtotal: float, is_member: bool) -> float:
    if is_member:
        return subtotal * (1 - MEMBER_DISCOUNT_RATE)
    return subtotal


def apply_tax(amount: float) -> float:
    return amount * (1 + TAX_RATE)


def calculate_order_total(price: float, quantity: int, is_member: bool) -> float:
    subtotal = calculate_subtotal(price, quantity)
    discounted = apply_member_discount(subtotal, is_member)
    return apply_tax(discounted)