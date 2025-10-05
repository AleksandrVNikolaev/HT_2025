# -*- coding: utf-8 -*-
"""
Домашнее задание №13 — Сетевое взаимодействие.
Получение данных из внешнего API (Bubble API с кадастровыми участками).
"""

import json
import requests
from typing import Any, Dict, List, Optional


class Rosreestr2Coord:
    """Класс для получения кадастровых данных с Bubble API."""

    BUBBLE_URL = "https://aleksandrvnikolaev-22756.bubbleapps.io/api/1.1/obj/plot"

    def __init__(
        self,
        timeout: int = 10,
        save_path: str = "rosreestr_data.json",
        limit: Optional[int] = 10,
    ) -> None:
        self._timeout = timeout
        self._save_path = save_path
        self._limit = limit

    def start(self) -> List[Dict[str, Any]]:
        """Основной метод: получает данные и сохраняет их в JSON."""
        print(f"\nПолучаю данные с Bubble API ({self.BUBBLE_URL})")
        data = self._fetch_from_bubble()
        parsed = self._parse_bubble(data)
        self._save_json(parsed)
        self._print_summary(parsed)
        return parsed

    def _fetch_from_bubble(self) -> Dict[str, Any]:
        """Отправляет запрос к API Bubble и возвращает JSON."""
        resp = requests.get(self.BUBBLE_URL, timeout=self._timeout)
        resp.raise_for_status()
        return resp.json()

    def _parse_bubble(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Извлекает ключевые поля из структуры Bubble API."""
        results = data.get("response", {}).get("results", [])
        parsed: List[Dict[str, Any]] = []
        for count, item in enumerate(results[: self._limit or len(results)], start=1):
            geojson_raw = item.get("geojson")
            if not geojson_raw:
                continue
            try:
                geo = json.loads(geojson_raw)
                props = geo.get("properties", {})
            except Exception:
                continue
            parsed.append(
                {
                    "cadnum": props.get("cadnum"),
                    "address": props.get("address"),
                    "area": props.get("area"),
                    "category": props.get("category"),
                    "cost": props.get("cost"),
                    "updated_at": props.get("updated_at"),
                }
            )
        return parsed

    def _save_json(self, data: Any) -> None:
        """Сохраняет результат в JSON."""
        with open(self._save_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Данные сохранены в {self._save_path}\n")

    def _print_summary(self, data: Any) -> None:
        """Выводит краткий отчёт в консоль."""
        print("======================================")
        print("Источник: Bubble API (данные кадастровых участков)")
        print(f"Получено объектов: {len(data)}")
        for i, p in enumerate(data, start=1):
            print(f"{i}. {p.get('cadnum')} | {p.get('address')} | {p.get('cost')}")
        print("======================================\n")


if __name__ == "__main__":
    parser = Rosreestr2Coord(limit=10)
    parser.start()
