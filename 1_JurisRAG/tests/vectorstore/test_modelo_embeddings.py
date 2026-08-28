from vectorstore.modelo_embeddings import criar_gerador_embeddings


class _ModeloFalso:
    def __init__(self):
        self.chamadas: list[str] = []

    def encode(self, texto, normalize_embeddings=True):
        self.chamadas.append(texto)
        return [0.1, 0.2, 0.3, 0.4]


def test_gerador_aplica_prefixo_e_retorna_vetor_do_modelo():
    modelo_falso = _ModeloFalso()
    gerar = criar_gerador_embeddings(prefixo="passage: ", carregador=lambda nome: modelo_falso)

    vetor = gerar("texto de exemplo")

    assert vetor == [0.1, 0.2, 0.3, 0.4]
    assert modelo_falso.chamadas == ["passage: texto de exemplo"]


def test_prefixos_de_passagem_e_consulta_sao_diferentes():
    modelo_falso = _ModeloFalso()

    def carregar(nome: str) -> _ModeloFalso:
        return modelo_falso

    gerar_passagem = criar_gerador_embeddings(prefixo="passage: ", carregador=carregar)
    gerar_consulta = criar_gerador_embeddings(prefixo="query: ", carregador=carregar)

    gerar_passagem("acórdão")
    gerar_consulta("pergunta do usuário")

    assert modelo_falso.chamadas == ["passage: acórdão", "query: pergunta do usuário"]


def test_determinismo_mesma_entrada_mesma_saida():
    modelo_falso = _ModeloFalso()
    gerar = criar_gerador_embeddings(carregador=lambda nome: modelo_falso)

    assert gerar("texto") == gerar("texto")
