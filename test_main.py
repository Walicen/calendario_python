from textwrap import dedent

from calendario import busca_feriados, apresentacao, gera_datas


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

    def test_gerar_datas(self):
        bisexto = gera_datas(2024, 2024)
        data = gera_datas(2021, 2021)
        assert len(bisexto) == 366
        assert len(data) == 365
        assert bisexto[59].numero_dia ==29
        assert data[0].numero_dia == 1
        assert data[95].trimestre == '2º Tri/21'
        assert data[181].trimestre == '3º Tri/21'
        assert data[277].trimestre == '4º Tri/21'

