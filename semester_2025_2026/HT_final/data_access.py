"""
Краткое описание:
1) Парсер получает кадастровые данные локально через утилиту rosreestr2coord
(стабильнее прямых запросов к pkk.rosreestr.ru).
2) models.py содержит модель Parcel — структура полей (кадастр, адрес, площадь,
категория, цена, координаты, дата).
3) parser_rosreestr.py формирует/обновляет rosreestr_data.json, сохраняя данные
из .geojson/.kml.
4) data_access.py читает JSON, выводит читабельную таблицу (перенос длинных строк),
считает суммарную и среднюю площадь, экспортирует CSV.
(подробное описание см. в файле README.md)
"""

from __future__ import annotations
import csv
import json
from decimal import Decimal
from pathlib import Path
from textwrap import wrap
from typing import Iterable, List
from models import Parcel

COLS = [
    ("Кадастровый номер", 22),
    ("Адрес", 60),
    ("Площадь, м²", 12),
    ("Категория", 32),
    ("Собственность", 14),
    ("Стоимость, ₽", 14),
    ("Дата обнов.", 12),
]


class RosreestrData:
    """Класс для анализа сохранённых данных."""

    def __init__(self, json_path: str | Path | None = None) -> None:
        base = Path(__file__).resolve().parent
        self._path = Path(json_path) if json_path else base / "parsed_data" / "rosreestr_data.json"
        self._items: List[Parcel] = []
        self._load()

    def _load(self) -> None:
        if not self._path.exists():
            raise FileNotFoundError(f"Файл данных не найден: {self._path}")
        with self._path.open("r", encoding="utf-8") as f:
            raw = json.load(f)
        self._items = [Parcel.from_dict(obj) for obj in raw if isinstance(obj, dict)]

    def print_report(self) -> None:
        print(f"[OK] Загружено {len(self._items)} участков из {self._path}\n")

        widths = [w for _, w in COLS]
        headers = [h for h, _ in COLS]
        line = "-" * (sum(widths) + len(widths) - 1)

        print("📋 Подробный отчёт по всем участкам:")
        print(line)
        print(self._fmt_row(headers, widths))
        print(line)

        for p in self._items:
            rows = self._wrap_row([
                p.cadastral_number or "",
                p.address or "—",
                f"{p.area_m2:.0f}" if p.area_m2 else "—",
                p.category or "—",
                p.ownership or "—",
                f"{p.price_rub:.0f}" if p.price_rub else "—",
                p.updated_at.isoformat() if p.updated_at else "—",
            ], widths)
            for r in rows:
                print(self._fmt_row(r, widths))
            print()  # отступ между участками
        print(line)

        areas = [p.area_m2 for p in self._items if p.area_m2]
        if areas:
            avg = sum(areas) / len(areas)
            total = sum(areas)
            print(f"Средняя площадь: {avg:.2f} м²")
            print(f"Суммарная площадь: {total:.2f} м²")
        else:
            print("Средняя площадь: —")
            print("Суммарная площадь: —")

    def export_csv(self, csv_path: str | Path | None = None) -> Path:
        """Экспорт данных в CSV с UTF-8 BOM (корректное открытие в Excel)."""
        out = Path(csv_path) if csv_path else Path(__file__).resolve().parent / "rosreestr_report.csv"
        with out.open("w", encoding="utf-8-sig", newline="") as f:  # исправлено!
            writer = csv.writer(f, delimiter=";")
            writer.writerow([h for h, _ in COLS])
            for p in self._items:
                writer.writerow([
                    p.cadastral_number or "",
                    p.address or "",
                    f"{p.area_m2:.0f}" if p.area_m2 else "",
                    p.category or "",
                    p.ownership or "",
                    f"{p.price_rub:.0f}" if p.price_rub else "",
                    p.updated_at.isoformat() if p.updated_at else "",
                ])
        return out

    @staticmethod
    def _wrap_row(values: List[str], widths: List[int]) -> List[List[str]]:
        wrapped = [wrap(v, w) or [""] for v, w in zip(values, widths)]
        height = max(len(c) for c in wrapped)
        for i, c in enumerate(wrapped):
            if len(c) < height:
                wrapped[i] += [""] * (height - len(c))
        return [list(row) for row in zip(*wrapped)]

    @staticmethod
    def _fmt_row(values: List[str], widths: List[int]) -> str:
        return " ".join(v.ljust(w)[:w] for v, w in zip(values, widths))


def main() -> None:
    db = RosreestrData()
    db.print_report()
    out = db.export_csv()
    print(f"[OK] Данные экспортированы в файл: {out}")


if __name__ == "__main__":
    main()
