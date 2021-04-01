from textwrap import dedent

from calendario import busca_feriados, apresentacao


class TestMain:

    def test_busca_feriados(self):
        lista = busca_feriados('2021')
        print(apresentacao(lista))
        assert apresentacao(lista) == dedent('''\
                Carnaval na data 15/02/2021 do tipo 4
                Carnaval na data 16/02/2021 do tipo 4
                Carnaval na data 17/02/2021 do tipo 4
                Corpus Christi na data 03/06/2021 do tipo 4
                Dia do Professor na data 15/10/2021 do tipo 4
                Dia do Servidor Público na data 28/10/2021 do tipo 4'''
        )