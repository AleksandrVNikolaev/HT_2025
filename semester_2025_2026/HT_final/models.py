from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, date
from decimal import Decimal
from typing import Any, Dict, Optional


@dataclass
class Parcel:
    """Модель данных об участке Росреестра."""
    cadastral_number: str
    address: Optional[str] = None
    area_m2: Optional[Decimal] = None
    category: Optional[str] = None
    price_rub: Optional[Decimal] = None
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None
    updated_at: Optional[date] = None

    def to_dict(self) -> Dict[str, Any]:
        """Сериализация в JSON-совместимый словарь."""
        return {
            'cadastral_number': self.cadastral_number,
            'address': self.address,
            'area_m2': str(self.area_m2) if self.area_m2 else None,
            'category': self.category,
            'price_rub': str(self.price_rub) if self.price_rub else None,
            'latitude': str(self.latitude) if self.latitude else None,
            'longitude': str(self.longitude) if self.longitude else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    @classmethod
    def from_dict(cls, raw: Dict[str, Any]) -> Parcel:
        """Десериализация из JSON."""
        def _dec(val: Any) -> Optional[Decimal]:
            return Decimal(str(val)) if val not in (None, '', 'None') else None

        def _date(val: Any) -> Optional[date]:
            if not val:
                return None
            try:
                return datetime.fromisoformat(str(val)).date()
            except ValueError:
                return None

        return cls(
            cadastral_number=str(raw.get('cadastral_number', '')).strip(),
            address=raw.get('address'),
            area_m2=_dec(raw.get('area_m2')),
            category=raw.get('category'),
            price_rub=_dec(raw.get('price_rub')),
            latitude=_dec(raw.get('latitude')),
            longitude=_dec(raw.get('longitude')),
            updated_at=_date(raw.get('updated_at')),
        )
