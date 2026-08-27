from __future__ import annotations

from .dominio import DocumentoJurisprudencial

CAMPOS_OBRIGATORIOS = ("tribunal", "numero_processo")


class RegistroInvalidoError(ValueError):
    def __init__(self, motivo: str, registro: dict):
        super().__init__(motivo)
        self.motivo = motivo
        self.registro = registro


def parse_documento(registro: dict) -> DocumentoJurisprudencial:
    for campo in CAMPOS_OBRIGATORIOS:
        if not registro.get(campo):
            raise RegistroInvalidoError(f"campo obrigatório ausente: {campo}", registro)

    return DocumentoJurisprudencial(
        id=registro.get("id") or f"{registro['tribunal']}-{registro['numero_processo']}",
        tribunal=registro["tribunal"],
        numero_processo=registro["numero_processo"],
        relator=registro.get("relator"),
        data_julgamento=registro.get("data_julgamento"),
        ementa=registro.get("ementa"),
        acordao_texto=registro.get("acordao_texto"),
        metadata=registro.get("metadata", {}),
    )
