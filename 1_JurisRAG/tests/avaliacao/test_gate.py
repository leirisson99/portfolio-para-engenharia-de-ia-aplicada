from avaliacao.gate import avaliar_threshold


def test_avaliar_threshold_aprova_quando_todas_as_metricas_atingem_o_limite():
    resultados = {"faithfulness": 0.9, "context_precision": 0.86}
    thresholds = {"faithfulness": 0.85, "context_precision": 0.85}

    assert avaliar_threshold(resultados, thresholds) is True


def test_avaliar_threshold_aprova_quando_metrica_e_exatamente_igual_ao_limite():
    assert avaliar_threshold({"faithfulness": 0.85}, {"faithfulness": 0.85}) is True


def test_avaliar_threshold_bloqueia_quando_uma_metrica_fica_abaixo_do_limite():
    resultados = {"faithfulness": 0.70, "context_precision": 0.90}
    thresholds = {"faithfulness": 0.85, "context_precision": 0.85}

    assert avaliar_threshold(resultados, thresholds) is False


def test_avaliar_threshold_considera_apenas_metricas_com_threshold_definido():
    resultados = {"faithfulness": 0.90, "metrica_extra_sem_threshold": 0.0}
    thresholds = {"faithfulness": 0.85}

    assert avaliar_threshold(resultados, thresholds) is True
