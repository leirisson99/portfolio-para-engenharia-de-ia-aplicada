from ingestao.normalizacao import (
    normalizar,
    normalizar_espacamento_e_encoding,
    remover_ruido_html,
)


def test_remove_tags_html_aninhadas():
    bruto = "<div><p>Texto <b>importante</b></p></div>"

    resultado = remover_ruido_html(bruto)

    assert "<" not in resultado
    assert ">" not in resultado


def test_remove_entidades_html():
    bruto = "A&nbsp;B &amp; C"

    assert remover_ruido_html(bruto) == "A B & C"


def test_texto_sem_ruido_eh_noop():
    limpo = "Texto já limpo, sem marcação."

    assert remover_ruido_html(limpo) == limpo


def test_normaliza_espacamento_multiplos_espacos_e_tabs():
    bruto = "Texto   com \t\t espaços   e\ttabs"

    assert normalizar_espacamento_e_encoding(bruto) == "Texto com espaços e tabs"


def test_normaliza_remove_caracteres_de_controle():
    bruto = "Texto\x0ccom\x00quebra de página"

    resultado = normalizar_espacamento_e_encoding(bruto)

    assert "\x0c" not in resultado
    assert "\x00" not in resultado


def test_normaliza_remove_caractere_de_substituicao_unicode():
    bruto = "Pedido de reconsidera��o recebido"

    resultado = normalizar_espacamento_e_encoding(bruto)

    assert "�" not in resultado


def test_normalizar_compoe_limpeza_html_e_espacamento():
    bruto = "<p>Texto   com <b>ruído</b>&nbsp;HTML</p>"

    texto_normalizado = normalizar(bruto)

    assert texto_normalizado.valor == "Texto com ruído HTML"
