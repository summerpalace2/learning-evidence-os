"""First-run configuration and capability discovery for the local runtime."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Union


MODES = ("study", "interview", "exam", "practice")
ADAPTERS = ("local", "notion", "google-drive", "google-sheets", "obsidian", "github-issues", "feishu")
IMPLEMENTED = {"local": "implemented"}


def build_config(
    *,
    profile: str = "generic",
    mode: str = "study",
    storage_root: Union[Path, str] = ".learning-evidence",
    sources: Iterable[str] = (),
    requested_adapters: Iterable[str] = ("local",),
) -> Dict[str, object]:
    profile = profile.strip() or "generic"
    if mode not in MODES:
        raise ValueError(f"不支持的学习模式：{mode}，可选值：{', '.join(MODES)}")
    requested = _unique([item.strip() for item in requested_adapters if item.strip()])
    unknown = [item for item in requested if item not in ADAPTERS]
    if unknown:
        raise ValueError(f"不支持的 Adapter：{', '.join(unknown)}")
    if "local" not in requested:
        requested.insert(0, "local")
    root = Path(storage_root).expanduser().resolve()
    capabilities = {
        name: {
            "status": IMPLEMENTED.get(name, "planned_not_implemented"),
            "canRead": name in IMPLEMENTED,
            "canWrite": name in IMPLEMENTED,
        }
        for name in requested
    }
    config = {
        "configVersion": 1,
        "profile": profile,
        "mode": mode,
        "storage": {"kind": "local-json", "root": str(root)},
        "sources": list(sources),
        "requestedAdapters": requested,
        "capabilities": capabilities,
        "privacy": {
            "publicRepo": False,
            "allowExternalWrite": False,
            "personalDataRoot": str(root),
        },
        "configuredAt": datetime.now(timezone.utc).isoformat(),
    }
    return validate_config(config)


def validate_config(config: Dict[str, object]) -> Dict[str, object]:
    """Reject malformed or unsafe configuration before it reaches the runtime."""

    if not isinstance(config, dict):
        raise ValueError("配置必须是 JSON 对象")
    if config.get("configVersion") != 1:
        raise ValueError("不支持的配置版本")
    if not isinstance(config.get("profile"), str) or not str(config["profile"]).strip():
        raise ValueError("配置缺少 profile")
    if config.get("mode") not in MODES:
        raise ValueError("配置包含无效 mode")
    storage = config.get("storage")
    if not isinstance(storage, dict) or storage.get("kind") != "local-json" or not storage.get("root"):
        raise ValueError("配置必须使用有效的 local-json storage")
    requested = config.get("requestedAdapters")
    if not isinstance(requested, list) or any(item not in ADAPTERS for item in requested):
        raise ValueError("配置缺少 requestedAdapters")
    capabilities = config.get("capabilities")
    local_capability = capabilities.get("local") if isinstance(capabilities, dict) else None
    if not isinstance(local_capability, dict) or local_capability.get("status") != "implemented":
        raise ValueError("配置必须保留已实现的 local 能力")
    privacy = config.get("privacy")
    if not isinstance(privacy, dict) or privacy.get("publicRepo") is not False:
        raise ValueError("个人运行配置不能标记为 publicRepo")
    return config


def interactive_setup(default_root: Union[Path, str] = ".learning-evidence") -> Dict[str, object]:
    """Ask only the choices needed to establish a safe first local run."""

    print("Learning Evidence OS 首次配置（外部 Adapter 目前只登记能力，不会伪造写回）")
    profile = _ask("学习领域 Profile", "generic")
    mode = _ask("学习模式：study / interview / exam / practice", "study")
    sources_text = _ask("已有资料位置（多个用逗号分隔，可留空）", "")
    adapters_text = _ask(
        "你已有的存储或连接器（local/notion/google-drive/google-sheets，可多个）",
        "local",
    )
    config = build_config(
        profile=profile,
        mode=mode,
        storage_root=default_root,
        sources=_csv(sources_text),
        requested_adapters=_csv(adapters_text) or ["local"],
    )
    unavailable = [
        name for name, capability in config["capabilities"].items() if capability["status"] != "implemented"
    ]
    if unavailable:
        print("未实现的连接器将保持计划状态，不参与持久化：" + ", ".join(unavailable))
    print("已选择可验证的本地存储：" + str(config["storage"]["root"]))
    return config


def _ask(label: str, default: str) -> str:
    try:
        value = input(f"{label} [{default}]：").strip()
    except EOFError:
        print()
        return default
    return value or default


def _csv(value: str) -> List[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def _unique(values: List[str]) -> List[str]:
    result: List[str] = []
    for value in values:
        if value not in result:
            result.append(value)
    return result
