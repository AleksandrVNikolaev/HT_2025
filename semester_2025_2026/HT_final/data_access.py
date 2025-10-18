from __future__ import annotations
import json
from pathlib import Path
from typing import List, Optional
from decimal import Decimal
from datetime import date
from models import Parcel


class RosreestrData:
    """Класс для работы с сохранёнными данными об участках."""

    def __init__(self, json_path: str | Path = None) -> None:
        base_dir = Path(__file__).resolve().parent
        self._path = Path(json_path) if json_path else base_dir / 'parsed_data' / 'rosreestr_data.json'
        self._items: List[Parcel] = []
        self._load()

    def _load(self) -> None:
        """Загружает данные из JSON."""
        if not self._path.exists():
            raise FileNotFoundError(f'Файл данных не найден: {self._path}')
        with self._path.open('r', encoding='utf-8') as f:
            raw = json.load(f)
        self._items = [Parcel.from_dict(obj) for obj in raw]

    # --- Методы доступа ---
    def count(self) -> int:
        """Количество участков в наборе данных."""
        return len(self._items)

    def by_cadastral_number(self, cn: str) -> Optional[Parcel]:
        """Находит участок по кадастровому номеру."""
        cn = cn.strip()
        return next((p for p in self._items if p.cadastral_number == cn), None)

    def filter_by_area(self, min_area: Optional[Decimal] = None, max_area: Optional[Decimal] = None) -> List[Parcel]:
        """Фильтрует участки по площади."""
        def ok(p: Parcel) -> bool:
            if p.area_m2 is None:
                return False
            if min_area and p.area_m2 < min_area:
                return False
            if max_area and p.area_m2 > max_area:
                return False
            return True
        return [p for p in self._items if ok(p)]

    def last_update_date(self) -> Optional[date]:
        """Последняя дата обновления среди всех участков."""
        dates = [p.updated_at for p in self._items if p.updated_at]
        return max(dates) if dates else None

    def average_area(self) -> Optional[Decimal]:
        """Средняя площадь участков."""
        areas = [p.area_m2 for p in self._items if p.area_m2]
        if not areas:
            return None
        return sum(areas) / len(areas)