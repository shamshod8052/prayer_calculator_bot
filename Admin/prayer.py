from dataclasses import dataclass
from datetime import datetime, time
from typing import Dict, Any
import httpx


def parse_time(time_str: str) -> time:
    """'HH:MM' ko‘rinishidagi stringni datetime.time formatiga o‘tkazish"""
    return datetime.strptime(time_str, "%H:%M").time()


@dataclass
class PrayerTime:
    BOMDOD: time
    QUYOSH: time
    PESHIN: time
    ASR: time
    SHOM: time
    XUFTON: time

    @staticmethod
    def from_dict(data: Dict[str, str]) -> 'PrayerTime':
        return PrayerTime(
            BOMDOD=parse_time(data['tong_saharlik']),
            QUYOSH=parse_time(data['quyosh']),
            PESHIN=parse_time(data['peshin']),
            ASR=parse_time(data['asr']),
            SHOM=parse_time(data['shom_iftor']),
            XUFTON=parse_time(data['hufton']),
        )

    def __str__(self):
        return (
            f"— BOMDOD: {self.BOMDOD.strftime('%H:%M')}\n"
            f"— QUYOSH: {self.QUYOSH.strftime('%H:%M')}\n"
            f"— PESHIN: {self.PESHIN.strftime('%H:%M')}\n"
            f"— ASR: {self.ASR.strftime('%H:%M')}\n"
            f"— SHOM: {self.SHOM.strftime('%H:%M')}\n"
            f"— XUFTON: {self.XUFTON.strftime('%H:%M')}\n"
        )


class PrayerBase:
    BASE_URL = "https://islomapi.uz/api/present/day"

    def fetch_data(self, region: str) -> Dict[str, Any]:
        """API dan namoz vaqtlarini olish"""
        try:
            response = httpx.get(self.BASE_URL, params={"region": region})
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise ValueError(f"Namoz vaqtlarini olishda xatolik: {e}") from e


class PresentDay(PrayerBase):
    def __init__(self, name: str, region: str):
        data = self.fetch_data(region)

        self.name = name
        self.region = region
        self.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        self.weekday = data['weekday']
        self.hijri_month = data['hijri_date']['month']
        self.hijri_day = data['hijri_date']['day']
        self.prayer_time = PrayerTime.from_dict(data['times'])

    def __str__(self):
        return (
            f"«{self.name.capitalize()}» vaqti bo'yicha namoz vaqtlari:\n\n"
            f"Sana: {self.date.strftime('%Y-%m-%d')}, {self.weekday}\n"
            f"Hijriy: {self.hijri_day}-{self.hijri_month}\n\n"
            f"{self.prayer_time}"
        )
