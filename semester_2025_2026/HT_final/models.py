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

from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from typing import Any, Dict, Optional


@dataclass
class Parcel:
    """Модель данных об участке Росреестра."""
    cadastral_number: str
    address: Optional[str] = None
    area_m2: Optional[Decimal] = None
    category: Optional[str] = None
    ownership: Optional[str] = None
    right_type: Optional[str] = None
    price_rub: Optional[Decimal] = None
    updated_at: Optional[date] = None

    def to_dict(self) -> Dict[str, Any]:
        """Сериализация в JSON-совместимый словарь."""
        return {
            "cadastral_number": self.cadastral_number,
            "address": self.address,
            "area_m2": str(self.area_m2) if self.area_m2 is not None else None,
            "category": self.category,
            "ownership": self.ownership,
            "right_type": self.right_type,
            "price_rub": str(self.price_rub) if self.price_rub is not None else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    @classmethod
    def from_dict(cls, raw: Dict[str, Any]) -> "Parcel":
        """Десериализация из JSON."""
        def _dec(val: Any) -> Optional[Decimal]:
            if val in (None, "", "None"):
                return None
            try:
                return Decimal(str(val))
            except Exception:
                return None

        def _date(val: Any) -> Optional[date]:
            if not val:
                return None
            try:
                return datetime.fromisoformat(str(val)).date()
            except Exception:
                return None

        return cls(
            cadastral_number=str(raw.get("cadastral_number", "")).strip(),
            address=raw.get("address"),
            area_m2=_dec(raw.get("area_m2")),
            category=raw.get("category"),
            ownership=raw.get("ownership"),
            right_type=raw.get("right_type"),
            price_rub=_dec(raw.get("price_rub")),
            updated_at=_date(raw.get("updated_at")),
        )