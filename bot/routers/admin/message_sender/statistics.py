import asyncio
import datetime
import logging
from dataclasses import dataclass, field
from typing import ClassVar, Dict, Optional, Tuple, List

logger = logging.getLogger(__name__)


@dataclass
class MailingStatistics:
    processes: ClassVar[Dict[int, 'MailingStatistics']] = {}
    total: int
    success: int = 0
    failed: int = 0
    blocked: int = 0
    invalid: int = 0
    stop: bool = False
    start_time: datetime.datetime = field(default_factory=lambda: datetime.datetime.now())
    stop_time: Optional[datetime.datetime] = None
    sleep_intervals: List[Tuple[datetime.datetime, float]] = field(default_factory=list)
    _lock: asyncio.Lock = field(default_factory=asyncio.Lock, init=False)

    @classmethod
    def get_process(cls, process_id):
        if process_id in cls.processes:
            return cls.processes[process_id]

    @property
    def progress(self) -> float:
        return (self.processed_num / self.total * 100) if self.total else 0.0

    @property
    def processed_num(self) -> int:
        return self.success + self.failed + self.blocked + self.invalid

    @property
    def elapsed_time(self) -> datetime.timedelta:
        return (self.stop_time or datetime.datetime.now()) - self.start_time

    @classmethod
    def start(cls, user_id: int, total: int) -> int:
        process_id = hash(f"{user_id}_{datetime.datetime.now().timestamp()}")
        cls.processes[process_id] = cls(total)
        return process_id

    @classmethod
    async def update_counter(cls, process_id: int, counter: str, value: int = 1):
        if process := cls.processes.get(process_id):
            async with process._lock:
                setattr(process, counter, getattr(process, counter) + value)

    @classmethod
    def stop_process(cls, process_id: int):
        if process := cls.processes.get(process_id):
            process.stop = True
            process.stop_time = datetime.datetime.now()

    @classmethod
    def record_sleep(cls, process_id: int, duration: float):
        if process := cls.processes.get(process_id):
            process.sleep_intervals.append((datetime.datetime.now(), duration))

    def get_stats(self) -> Dict[str, str]:
        sleep_end = max(
            (start + datetime.timedelta(seconds=dur) for start, dur in self.sleep_intervals),
            default=None
        )

        return {
            "total": str(f"{self.processed_num}/{self.total}"),
            "success": str(self.success),
            "failed": str(self.failed),
            "blocked": str(self.blocked),
            "invalid": str(self.invalid),
            "start_time": str(self.start_time),
            "stop_time": str(self.stop_time if self.stop_time else '-'),
            "progress": f"{self.progress:.1f}%",
            "elapsed": str(self.elapsed_time),
            "sleep_remaining": str(sleep_end - datetime.datetime.now()) if sleep_end else "0:00:00"
        }

    def format_stats(self) -> str:
        stats = self.get_stats()
        sleep_info = ''.join(
            f"\n⏸ {start.time()} - {dur}s"
            for start, dur in self.sleep_intervals
        )

        return (
            f"\n📊 Statistics:\n"
            f"📩 Total: {stats['total']}\n"
            f"✅ Success: {stats['success']}\n"
            f"❌ Failed: {stats['failed']}\n"
            f"🚫 Blocked: {stats['blocked']}\n"
            f"⚠️ Invalid: {stats['invalid']}\n\n"
            f"⏳ Started time: {stats['start_time']}\n"
            f"⏳ Stopped time: {stats['stop_time']}\n\n"
            f"📈 Progress: {stats['progress']}\n"
            f"⏳ Elapsed: {stats['elapsed']}\n"
            f"💤 Remaining sleep: {stats['sleep_remaining']}\n"
            f"🕒 Recent sleeps: {sleep_info if sleep_info else '✅'}"
        )