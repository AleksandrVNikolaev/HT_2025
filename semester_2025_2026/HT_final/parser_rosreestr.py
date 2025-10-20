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
import json
import subprocess
from datetime import date
from decimal import Decimal
from pathlib import Path
from typing import Dict, Iterable, List, Optional
from textwrap import wrap
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


class Parser:
    """Парсер, запускающий rosreestr2coord и сохраняющий данные в JSON."""

    def __init__(self) -> None:
        base = Path(__file__).resolve().parent
        self.project_dir = base
        self.output_dir = base / "output"
        self.geojson_dir = self.output_dir / "geojson"
        self.kml_dir = self.output_dir / "kml"
        self.data_dir = base / "parsed_data"
        self.data_file = self.data_dir / "rosreestr_data.json"
        self._ensure_dirs()

    def start(self) -> None:
        """Запуск парсера"""
        raw = input(
            "Введите кадастровые номера (через запятую, например "
            "39:05:030616:109,39:05:030616:110): "
        ).strip()
        codes = [c.strip() for c in raw.split(",") if c.strip()]
        if not codes:
            print("Ничего не введено.")
            return

        print()
        items = self._load_existing()
        index: Dict[str, Parcel] = {p.cadastral_number: p for p in items}
        new_items: List[Parcel] = []

        for cn in codes:
            print(f"→ Получаю данные по участку {cn} через rosreestr2coord...")
            gj_path = self._geojson_path(cn)
            if not gj_path.exists():
                ok = self._run_cli(cn)
                if not ok or not gj_path.exists():
                    print(f"[WARN] Файл GeoJSON не найден: {gj_path}")
                    continue

            parcel = self._parcel_from_geojson_file(gj_path, fallback_cadnum=cn)
            if parcel:
                index[parcel.cadastral_number] = parcel
                new_items.append(parcel)
                print(f"[OK] Прочитан файл: {gj_path}")
            else:
                print(f"[WARN] Не удалось разобрать файл: {gj_path}")

        all_items = list(index.values())
        self._save(all_items)
        print(f"\n[OK] Сохранено: {self.data_file}\n")

        # выводим только результаты текущего запроса
        self._print_table(new_items)

    def _ensure_dirs(self) -> None:
        self.geojson_dir.mkdir(parents=True, exist_ok=True)
        self.kml_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def _geojson_path(self, cadnum: str) -> Path:
        fname = cadnum.replace(":", "_") + ".geojson"
        return self.geojson_dir / fname

    def _run_cli(self, cadnum: str) -> bool:
        exe = self._guess_executable()
        try:
            cp = subprocess.run(
                [str(exe), "-c", cadnum, "-o", str(self.output_dir)],
                cwd=self.project_dir,
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
        except FileNotFoundError:
            print("[WARN] rosreestr2coord не найден. Установите пакет в .venv.")
            return False
        if "The request timed out" in (cp.stdout or ""):
            return False
        return True

    def _guess_executable(self) -> Path | str:
        venv = Path(__file__).resolve().parents[2] / ".venv" / "Scripts" / "rosreestr2coord.exe"
        if venv.exists():
            return venv
        return "rosreestr2coord"

    def _parcel_from_geojson_file(self, path: Path, fallback_cadnum: str) -> Optional[Parcel]:
        try:
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            return None

        props: Optional[dict] = None
        if isinstance(data, dict) and data.get("type") == "Feature":
            props = data.get("properties") or {}
        elif isinstance(data, dict) and data.get("type") == "FeatureCollection":
            feats = data.get("features") or []
            if feats and isinstance(feats[0], dict):
                props = feats[0].get("properties") or {}

        if not props:
            return None

        options = props.get("options") or {}
        cadnum = (
            str(options.get("cad_num"))
            or str(props.get("externalKey"))
            or str(props.get("label"))
            or fallback_cadnum
        ).strip()

        address = options.get("readable_address") or props.get("descr")
        area_val = (
            options.get("specified_area")
            or options.get("land_record_area")
            or options.get("area")
        )
        category = (
            options.get("land_record_category_type")
            or props.get("categoryName")
        )
        ownership = options.get("ownership_type")
        right_type = options.get("right_type")
        price_val = options.get("cost_value")
        upd_date = (
            options.get("cost_registration_date")
            or options.get("land_record_reg_date")
        )

        return Parcel(
            cadastral_number=cadnum,
            address=address,
            area_m2=Decimal(str(area_val)) if area_val else None,
            category=category,
            ownership=ownership,
            right_type=right_type,
            price_rub=Decimal(str(price_val)) if price_val else None,
            updated_at=date.fromisoformat(upd_date) if upd_date else None,
        )

    def _load_existing(self) -> List[Parcel]:
        if not self.data_file.exists():
            return []
        with self.data_file.open("r", encoding="utf-8") as f:
            raw = json.load(f)
        return [Parcel.from_dict(obj) for obj in raw if isinstance(obj, dict)]

    def _save(self, items: Iterable[Parcel]) -> None:
        data = [p.to_dict() for p in items]
        with self.data_file.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _print_table(self, items: List[Parcel]) -> None:
        if not items:
            print("❌ Нет данных для вывода.")
            return

        widths = [w for _, w in COLS]
        headers = [h for h, _ in COLS]
        line = "-" * (sum(widths) + len(widths) - 1)

        print("📋 Результаты текущего запроса:")
        print(line)
        print(self._fmt_row(headers, widths))
        print(line)

        for p in items:
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
            print()  # ← отступ между участками
        print(line)

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


if __name__ == "__main__":
    Parser().start()