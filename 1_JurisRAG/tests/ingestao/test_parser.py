import pytest

from ingestao.dominio import DocumentoJurisprudencial
from ingestao.parser import RegistroInvalidoError, parse_documento


def test_mapeia_registro_completo_para_documento():
    registro = {
        "tribunal": "STJ",
        "numero_processo": "REsp 123456/SP",
        "relator": "Min. Fulano de Tal",
        "data_julgamento": "2023-05-10",
        "ementa": "Ementa de exemplo.",
        "acordao_texto": "Texto do acórdão.",
    }

    documento = parse_documento(registro)

    assert isinstance(documento, DocumentoJurisprudencial)
    assert documento.tribunal == "STJ"
    assert documento.numero_processo == "REsp 123456/SP"
    assert documento.relator == "Min. Fulano de Tal"
    assert documento.ementa == "Ementa de exemplo."
    assert documento.acordao_texto == "Texto do acórdão."


def test_registro_sem_numero_processo_marca_invalido():
    registro = {"tribunal": "STJ", "relator": "Min. Fulano de Tal"}

    with pytest.raises(RegistroInvalidoError):
        parse_documento(registro)


def test_registro_sem_campos_opcionais_usa_none():
    registro = {"tribunal": "STJ", "numero_processo": "REsp 1/SP"}

    documento = parse_documento(registro)

    assert documento.relator is None
    assert documento.ementa is None
    assert documento.acordao_texto is None
