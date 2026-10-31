import json
from pathlib import Path
from datetime import datetime, timezone
from . import config


def data_dir() -> Path:
    return Path(config.DATA_DIR)


def load_json(name: str, default):
    path = data_dir() / name
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return default


def save_json(name: str, payload) -> None:
    folder = data_dir()
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / name
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    temp.replace(path)


def append_jsonl(name: str, payload: dict) -> None:
    folder = data_dir()
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / name
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")
