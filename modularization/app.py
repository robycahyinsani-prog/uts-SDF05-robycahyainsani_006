"""Entry point: orkestrasi reader, pricing, report_writer, summary_printer."""
from reader import read_orders
from pricing import calculate_order_total
from report_writer import write_report
from summary_printer import print_summary


def main():
    orders = read_orders("orders.csv")
    lines = []
    grand_total = 0.0

    for order in orders:
        total = calculate_order_total(
            order["price"], order["quantity"], order["is_member"]
        )
        grand_total += total
        lines.append(f"{order['item']}: {total:.2f}")

    write_report("report.txt", lines)
    print_summary(len(orders), grand_total)


if __name__ == "__main__":
    main()