"""Modul untuk menulis report ke file."""


def write_report(file_path: str, lines: list[str]) -> None:
    """Menulis list of string ke report.txt."""
    with open(file_path, mode="w", encoding="utf-8") as f:
        f.write("\n".join(lines))