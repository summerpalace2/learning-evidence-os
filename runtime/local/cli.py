"""Command line entrypoint for Bootstrap and local status checks."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List, Optional, Sequence

from .adapter import LocalAdapter
from .bootstrap import build_config, interactive_setup
from .workflow import LearningRuntime


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Learning Evidence OS local runtime")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init", help="运行首次 Bootstrap 配置")
    init.add_argument("--root", default=".learning-evidence")
    init.add_argument("--profile", default="generic")
    init.add_argument("--mode", default="study")
    init.add_argument("--sources", default="")
    init.add_argument("--adapters", default="local")
    init.add_argument("--non-interactive", action="store_true")

    status = subparsers.add_parser("status", help="查看配置、能力和对象数量")
    status.add_argument("--root", default=".learning-evidence")

    args = parser.parse_args(argv)
    if args.command == "init":
        adapter = LocalAdapter(args.root)
        config = (
            build_config(
                profile=args.profile,
                mode=args.mode,
                storage_root=args.root,
                sources=_csv(args.sources),
                requested_adapters=_csv(args.adapters) or ["local"],
            )
            if args.non_interactive
            else interactive_setup(args.root)
        )
        adapter.save_config(config)
        print(json.dumps(config, ensure_ascii=False, indent=2))
        return 0
    if args.command == "status":
        result = LearningRuntime(LocalAdapter(args.root)).status()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    return 2


def _csv(value: str) -> List[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


if __name__ == "__main__":
    raise SystemExit(main())
