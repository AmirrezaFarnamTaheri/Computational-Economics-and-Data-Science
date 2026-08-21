#!/usr/bin/env python3
"""Strict notebook-quality validation entry point for contributors and CI."""
from __future__ import annotations
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
raise SystemExit(subprocess.call([sys.executable, str(ROOT / "scripts" / "audit_curriculum_ast.py"), "--root", str(ROOT), "--strict"]))
