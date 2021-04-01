from textwrap import dedent

from calendario import busca_feriados, apresentacao


class TestMain:

    def test_busca_feriados(self):
        lista = busca_feriados('2021')
        print(apresentacao(lista))
        assert apresentacao(lista) == dedent('''\
                15/02/2021 Carnaval 4
                16/02/2021 Carnaval 4
                17/02/2021 Carnaval 4
                03/06/2021 Corpus Christi 4
                15/10/2021 Dia do Professor 4
                28/10/2021 Dia do Servidor Público 4'''
        )