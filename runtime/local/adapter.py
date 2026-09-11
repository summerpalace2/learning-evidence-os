"""Atomic JSON storage for the minimum viable Learning Evidence OS runtime."""

from __future__ import annotations

import json
import os
import re
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


class LocalAdapterError(RuntimeError):
    """Raised when local persistence cannot safely complete."""


KIND_DIRECTORIES = {
    "topic": "topics",
    "node": "nodes",
    "article": "articles",
    "question": "questions",
    "answer": "answers",
    "session": "sessions",
    "evidence": "evidence",
    "topic_state": "topic-states",
    "presentation": "presentations",
    "handoff": "handoffs",
    "acceptance_round": "acceptance-rounds",
    "coverage_finding": "coverage-findings",
}
SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


class LocalAdapter:
    """Store Core objects as inspectable JSON files under one private root."""

    def __init__(self, root: Union[Path, str]):
        self.root = Path(root).expanduser().resolve()
        self.objects_root = self.root / "objects"
        self.config_path = self.root / "config.json"

    def initialize(self) -> None:
        self.objects_root.mkdir(parents=True, exist_ok=True)
        for directory in KIND_DIRECTORIES.values():
            (self.objects_root / directory).mkdir(parents=True, exist_ok=True)

    def save_config(self, config: Dict[str, Any]) -> None:
        from .bootstrap import validate_config

        validate_config(config)
        self.initialize()
        _atomic_write_json(self.config_path, config)

    def load_config(self) -> Optional[Dict[str, Any]]:
        if not self.config_path.exists():
            return None
        try:
            config = json.loads(self.config_path.read_text(encoding="utf-8"))
            from .bootstrap import validate_config

            return validate_config(config)
        except (OSError, json.JSONDecodeError) as exc:
            raise LocalAdapterError(f"无法读取配置：{self.config_path}") from exc

    def save(self, kind: str, obj: Dict[str, Any], *, overwrite: bool = False) -> Path:
        path = self._object_path(kind, obj.get("id"))
        self.initialize()
        if path.exists() and not overwrite:
            raise LocalAdapterError(f"对象已存在，拒绝覆盖：{kind}/{obj['id']}")
        _atomic_write_json(path, obj)
        return path

    def update(self, kind: str, obj: Dict[str, Any]) -> Path:
        return self.save(kind, obj, overwrite=True)

    def get(self, kind: str, object_id: str) -> Optional[Dict[str, Any]]:
        path = self._object_path(kind, object_id)
        if not path.exists():
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise LocalAdapterError(f"无法读取对象：{kind}/{object_id}") from exc

    def require(self, kind: str, object_id: str) -> Dict[str, Any]:
        obj = self.get(kind, object_id)
        if obj is None:
            raise LocalAdapterError(f"找不到对象：{kind}/{object_id}")
        return obj

    def list(self, kind: str) -> List[Dict[str, Any]]:
        directory = self._directory(kind)
        if not directory.exists():
            return []
        result: List[Dict[str, Any]] = []
        for path in sorted(directory.glob("*.json")):
            try:
                result.append(json.loads(path.read_text(encoding="utf-8")))
            except (OSError, json.JSONDecodeError) as exc:
                raise LocalAdapterError(f"无法读取对象：{path}") from exc
        return result

    def counts(self) -> Dict[str, int]:
        return {kind: len(self.list(kind)) for kind in KIND_DIRECTORIES}

    def _directory(self, kind: str) -> Path:
        if kind not in KIND_DIRECTORIES:
            raise LocalAdapterError(f"不支持的对象类型：{kind}")
        return self.objects_root / KIND_DIRECTORIES[kind]

    def _object_path(self, kind: str, object_id: Any) -> Path:
        if not isinstance(object_id, str) or not SAFE_ID.fullmatch(object_id):
            raise LocalAdapterError(f"对象必须使用安全稳定 ID：{object_id!r}")
        return self._directory(kind) / f"{object_id}.json"


def _atomic_write_json(path: Path, value: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    temporary_name: Optional[str] = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent, delete=False, suffix=".tmp"
        ) as handle:
            temporary_name = handle.name
            handle.write(encoded)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_name, path)
    except OSError as exc:
        if temporary_name:
            try:
                os.unlink(temporary_name)
            except OSError:
                pass
        raise LocalAdapterError(f"本地写回失败，未声称成功：{path}") from exc
