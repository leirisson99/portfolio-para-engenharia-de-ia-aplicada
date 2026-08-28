from __future__ import annotations


def avaliar_threshold(
    resultados_por_metrica: dict[str, float], thresholds: dict[str, float]
) -> bool:
    """RF-6.2/RN03: uma Execução de Avaliação só passa se toda Métrica de
    Avaliação com Threshold definido atingir ou superar seu valor mínimo.
    """
    return all(
        resultados_por_metrica[nome] >= limite for nome, limite in thresholds.items()
    )
