import pytest

from avaliacao.metricas import agregar_metricas


def test_agregar_metricas_calcula_media_por_metrica_entre_os_casos():
    resultados_por_caso = [
        {"faithfulness": 1.0, "answer_relevancy": 0.5},
        {"faithfulness": 0.5, "answer_relevancy": 1.0},
    ]

    agregado = agregar_metricas(resultados_por_caso)

    assert agregado == {"faithfulness": 0.75, "answer_relevancy": 0.75}


def test_agregar_metricas_com_um_unico_caso_retorna_os_proprios_valores():
    resultados_por_caso = [{"faithfulness": 0.9}]

    assert agregar_metricas(resultados_por_caso) == {"faithfulness": 0.9}


def test_agregar_metricas_falha_com_lista_vazia():
    with pytest.raises(ValueError):
        agregar_metricas([])
