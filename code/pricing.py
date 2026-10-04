# Konstanta bernama (menghilangkan magic numbers)
MEMBER_DISCOUNT_RATE = 0.10   # diskon 10% untuk member
TAX_RATE = 0.11               # pajak 11%


def calculate_subtotal(price: float, quantity: int) -> float:
    """Menghitung subtotal sebelum diskon dan pajak."""
    return price * quantity


def apply_member_discount(subtotal: float, is_member: bool) -> float:
    """Menerapkan diskon member jika pembeli adalah member."""
    if is_member:
        return subtotal * (1 - MEMBER_DISCOUNT_RATE)
    return subtotal


def apply_tax(amount: float) -> float:
    """Menerapkan pajak pada amount."""
    return amount * (1 + TAX_RATE)


def calculate_order_total(price: float, quantity: int, is_member: bool) -> float:
    """Menghitung total order setelah diskon dan pajak."""
    subtotal = calculate_subtotal(price, quantity)
    discounted = apply_member_discount(subtotal, is_member)
    return apply_tax(discounted)