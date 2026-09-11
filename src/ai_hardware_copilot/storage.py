"""Atomic local persistence for replayable conference records."""

from __future__ import annotations

import json
import os
from pathlib import Path

from .models import ConferenceRecord


class ConferenceStore:
    def __init__(self, root: str | Path):
        self.root = Path(root)

    def save(self, record: ConferenceRecord) -> Path:
        conference_root = self.root / record.conference_id
        conference_root.mkdir(parents=True, exist_ok=True)
        destination = conference_root / "state.json"
        temporary = conference_root / "state.json.tmp"
        with temporary.open("w", encoding="utf-8", newline="\n") as handle:
            json.dump(record.as_dict(), handle, indent=2, sort_keys=True, ensure_ascii=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, destination)
        self._write_events(record, conference_root / "events.ndjson")
        return destination

    def load(self, conference_id: str) -> ConferenceRecord:
        source = self.root / conference_id / "state.json"
        with source.open("r", encoding="utf-8") as handle:
            value = json.load(handle)
        return ConferenceRecord.from_dict(value)

    @staticmethod
    def _write_events(record: ConferenceRecord, destination: Path) -> None:
        temporary = destination.with_suffix(".ndjson.tmp")
        with temporary.open("w", encoding="utf-8", newline="\n") as handle:
            for event in record.as_dict()["events"]:
                handle.write(json.dumps(event, sort_keys=True, ensure_ascii=False) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, destination)
