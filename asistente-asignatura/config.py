"""Project root path utilities.

This module centralises all directory path computation so that converters
and other scripts are never decoupled from the project structure via magic
parent traversals like ``Path(__file__).parent.parent.parent``.

Every sub-project (pdf2Markdown, markdown2Pdf) sits inside
``asistente-asignatura/scriptsAuxiliares/conversores/<name>/``.  The
``BASE_DIR`` computed here resolves to ``asistente-asignatura/`` which is
the natural root for the ``base_de_conocimiento`` and ``ejercicios`` trees.
"""

from __future__ import annotations

from pathlib import Path

__all__ = [
    "BASE_DIR",
    "BASE_DE_CONOCIMIENTO",
    "ENUNCIADOS_SINTETICOS",
    "ALUMNO_DIR",
    "ENUNCIADOS_SOLUCIONADOS",
    "SPECIAL_SCRIPTS_DIR",
]

# ---------------------------------------------------------------------------
# Resolve the base directory **relative to this file**.
#
# Currently::
#
#   /.../aedi-agent/asistente-asignatura/config.py
#
# Resolves to::
#
#   /.../aedi-agent/asistente-asignatura/
# ---------------------------------------------------------------------------
BASE_DIR: Path = Path(__file__).resolve().parent  # type: ignore[assignment]

# ── Data directories ────────────────────────────────────────────────────

BASE_DE_CONOCIMIENTO: Path = BASE_DIR / "base_de_conocimiento"

# Exercises generated/consumed by the AI assistant:
#   - enunciados_sinteticos:      AI-generated exercise statements
#   - alumno:  skeleton students must fill in
#   - resueltos:  student-solved exercises (reference/grading)
EJERCICIOS_DIR = BASE_DIR / "ejercicios"
ENUNCIADOS_SINTETICOS = EJERCICIOS_DIR / "enunciados_sinteticos"
ALUMNO_DIR = EJERCICIOS_DIR / "alumno"
# (Path used by the Markdown converter as a fallback target)
ENUNCIADOS_SOLUCIONADOS = EJERCICIOS_DIR / "resueltos"

# ── Scripts directory (scriptsAuxiliares) ───────────────────────────────

SPECIAL_SCRIPTS_DIR = BASE_DIR / "scriptsAuxiliares"
