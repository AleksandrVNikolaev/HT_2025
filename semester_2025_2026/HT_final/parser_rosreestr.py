from __future__ import annotations
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from decimal import Decimal
import requests
from models import Parcel


class ParserRosreestr:
    """Парсер данных Росреестра (интерактивный режим без сервера)."""

    BASE_URL = "https://pkk.rosreestr.ru/api/features/1"

    def __init__(self, timeout: int = 15, save_filename: str = "rosreestr_data.json") -> None:
        self._timeout = timeout
        self._save_path = Path(__file__).resolve().parent / "parsed_data" / save_filename
        self._save_path.parent.mkdir(parents=True, exist_ok=True)

    def start(self, cadastral_numbers: List[str]) -> List[Parcel]:
        """Основной метод: получает данные по кадастровым номерам."""
        results: List[Parcel] = []
        for cn in cadastral_numbers:
            data = self._fetch_one(cn)
            parcel = self._parse_one(data, cn)
            if parcel:
                results.append(parcel)
        self._save_json(results)
        self._print_summary(results)
        return results

    def _fetch_one(self, cadastral_number: str) -> Dict[str, Any]:
        """Делает запрос напрямую к API Росреестра."""
        url = f"{self.BASE_URL}?text={cadastral_number}"
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0 Safari/537.36"
            ),
            "Accept": "application/json, text/plain, */*",
            "Referer": "https://pkk.rosreestr.ru/",
        }

        try:
            response = requests.get(url, headers=headers, timeout=self._timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as exc:
            print(f"[WARN] Ошибка при запросе {cadastral_number}: {exc}")
            return {}

    def _parse_one(self, data: Dict[str, Any], cn: str) -> Optional[Parcel]:
        """Разбор структуры ответа Росреестра."""
        features = data.get("features")
        if not features:
            return None

        attrs = features[0].get("attrs", {})
        geom = features[0].get("geometry", {})

        lat = lon = None
        if geom.get("coordinates"):
            try:
                coords = geom["coordinates"]
                if isinstance(coords[0], (float, int)):
                    lon, lat = map(Decimal, coords)
                elif isinstance(coords[0], list):
                    lon, lat = map(Decimal, coords[0][0])
            except Exception:
                pass

        normalized = {
            "cadastral_number": attrs.get("cn") or cn,
            "address": attrs.get("address"),
            "area_m2": attrs.get("area_value"),
            "category": attrs.get("category_type"),
            "price_rub": attrs.get("cad_cost"),
            "latitude": lat,
            "longitude": lon,
            "updated_at": attrs.get("date_update") or attrs.get("date_cost"),
        }

        return Parcel.from_dict(normalized)

    def _save_json(self, data: List[Parcel]) -> None:
        """Сохраняет JSON в parsed_data/."""
        payload = [p.to_dict() for p in data]
        with self._save_path.open("w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=4)
        print(f"[OK] Сохранено: {self._save_path}")

    def _print_summary(self, data: List[Parcel]) -> None:
        """Печатает краткий отчёт."""
        print("\nКраткий отчёт по участкам:")
        for i, p in enumerate(data, start=1):
            print(f"{i}. {p.cadastral_number} — {p.address} — {p.area_m2} м²")


if __name__ == "__main__":
    # 🔹 Запрос кадастрового номера у пользователя
    user_input = input("Введите кадастровый номер участка (например 39:05:030616:109): ").strip()

    if not user_input:
        print("❌ Кадастровый номер не введён. Завершение работы.")
    else:
        parser = ParserRosreestr()
        parcels = parser.start([user_input])
        if parcels:
            p = parcels[0]
            print("\n📋 Информация об участке:")
            print(f"Кадастровый номер: {p.cadastral_number}")
            print(f"Адрес: {p.address}")
            print(f"Площадь: {p.area_m2} м²")
            print(f"Категория: {p.category}")
            print(f"Кадастровая стоимость: {p.price_rub} руб.")
            print(f"Дата обновления: {p.updated_at}")
        else:
            print("❌ Не удалось получить данные по этому участку.")