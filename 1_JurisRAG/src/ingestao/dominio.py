from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class TextoNormalizado:
    """Value Object imutável: texto após limpeza de HTML/ruído e normalização."""

    valor: str


@dataclass(frozen=True)
class DocumentoJurisprudencial:
    """Registro bruto de uma decisão do STJ, antes de qualquer transformação."""

    id: str
    tribunal: str
    numero_processo: str
    relator: str | None
    data_julgamento: str | None
    ementa: str | None
    acordao_texto: str | None
    metadata: dict = field(default_factory=dict)
