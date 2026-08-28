import json

import pytest

from avaliacao.dominio import CasoGolden
from avaliacao.golden_dataset import carregar_casos_golden
from avaliacao.validacao_golden import (
    CasoGoldenInvalidoError,
    validar_casos_regressao_preservados,
    validar_schema,
    validar_tamanho_dataset,
    validar_validador_humano,
)


def _caso(**overrides) -> CasoGolden:
    base = dict(
        id="GD-001",
        pergunta="Pergunta de teste?",
        resposta_referencia="Resposta de referência de teste.",
        tribunal="STJ",
        validado_por="Fulano de Tal",
        data_validacao="2026-08-27",
    )
    base.update(overrides)
    return CasoGolden(**base)


def test_carregar_casos_golden_le_jsonl_e_faz_parse_dos_campos(tmp_path):
    caminho = tmp_path / "casos.jsonl"
    caminho.write_text(
        "\n".join(
            [
                json.dumps(
                    {
                        "id": "GD-001",
                        "pergunta": "O que é dano moral?",
                        "resposta_referencia": "É a lesão a direito da personalidade.",
                        "tribunal": "STJ",
                        "validado_por": "Fulano de Tal",
                        "data_validacao": "2026-08-27",
                        "contexto_esperado": "trecho da ementa",
                        "origem": "curadoria",
                    },
                    ensure_ascii=False,
                ),
                "",  # linha em branco deve ser ignorada
            ]
        ),
        encoding="utf-8",
    )

    casos = carregar_casos_golden(caminho)

    assert len(casos) == 1
    assert casos[0].id == "GD-001"
    assert casos[0].pergunta == "O que é dano moral?"
    assert casos[0].contexto_esperado == "trecho da ementa"
    assert casos[0].origem == "curadoria"


def test_validar_schema_aceita_caso_com_campos_obrigatorios_preenchidos():
    validar_schema(_caso())  # não deve levantar


@pytest.mark.parametrize(
    "campo", ["pergunta", "resposta_referencia", "validado_por", "data_validacao"]
)
def test_validar_schema_rejeita_caso_com_campo_obrigatorio_vazio(campo):
    caso = _caso(**{campo: ""})

    with pytest.raises(CasoGoldenInvalidoError, match=campo):
        validar_schema(caso)


def test_validar_tamanho_dataset_aceita_entre_30_e_50_casos():
    casos = [_caso(id=f"GD-{i:03d}") for i in range(30)]
    validar_tamanho_dataset(casos)  # não deve levantar

    casos = [_caso(id=f"GD-{i:03d}") for i in range(50)]
    validar_tamanho_dataset(casos)  # não deve levantar


def test_validar_tamanho_dataset_rejeita_menos_de_30_ou_mais_de_50():
    with pytest.raises(CasoGoldenInvalidoError, match="RF01"):
        validar_tamanho_dataset([_caso(id=f"GD-{i:03d}") for i in range(29)])

    with pytest.raises(CasoGoldenInvalidoError, match="RF01"):
        validar_tamanho_dataset([_caso(id=f"GD-{i:03d}") for i in range(51)])


@pytest.mark.parametrize("marcador", ["", "ia", "IA", "auto", "gpt", "claude", "pendente"])
def test_validar_validador_humano_rejeita_marcadores_automaticos(marcador):
    caso = _caso(validado_por=marcador)

    with pytest.raises(CasoGoldenInvalidoError, match="RN05"):
        validar_validador_humano(caso)


def test_validar_validador_humano_aceita_nome_de_revisor():
    validar_validador_humano(_caso(validado_por="Leirisson Souza"))  # não deve levantar


def test_validar_casos_regressao_preservados_aceita_quando_nada_foi_removido():
    anteriores = [_caso(id="GD-001", origem="regressao"), _caso(id="GD-002")]
    atuais = [_caso(id="GD-001", origem="regressao"), _caso(id="GD-002"), _caso(id="GD-003")]

    validar_casos_regressao_preservados(anteriores, atuais)  # não deve levantar


def test_validar_casos_regressao_preservados_rejeita_remocao_de_caso_de_regressao():
    anteriores = [_caso(id="GD-001", origem="regressao"), _caso(id="GD-002")]
    atuais = [_caso(id="GD-002")]  # GD-001, caso de regressão, foi removido

    with pytest.raises(CasoGoldenInvalidoError, match="RN04"):
        validar_casos_regressao_preservados(anteriores, atuais)


def test_validar_casos_regressao_preservados_ignora_remocao_de_caso_nao_regressao():
    anteriores = [_caso(id="GD-001"), _caso(id="GD-002")]
    atuais = [_caso(id="GD-002")]  # GD-001 removido, mas não é caso de regressão

    validar_casos_regressao_preservados(anteriores, atuais)  # não deve levantar
