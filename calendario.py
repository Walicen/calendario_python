import time
from datetime import date
from requests import get
from collections import namedtuple

CODIGO_CIDADE = "4106902"

TOKEN = "d2FsaWNlbi5kYWxhenVhbmFAY3J1enZlcm1lbGhhcHIuY29tLmJyJmhhc2g9OTcwOTY4NDk"  # Todo pegar de arquivo .env

URL = "https://api.calendario.com.br/?json=true"

year_begin = 2000
year_end = 2050


def get_con(acessoBanco):
    #conn = oracle.connect(acessoBanco)
    #conn.autocommit = True
    #return conn
    pass

"""
1	Janeiro	  tem 31 dias
2	Fevereiro tem 28 dias (29 dias nos anos bissextos)
3	Março	  tem 31 dias
4	Abril	  tem 30 dias
5	Maio	  tem 31 dias
6	Junho	  tem 30 dias
7	Julho	  tem 31 dias
8	Agosto	  tem 31 dias
9	Setembro  tem 30 dias
10	Outubro	  tem 31 dias
11	Novembro  tem 30 dias
12	Dezembro  tem 31 dias

"""


class Calendario():
    weeks_days = ('Segunda-feira', 'Terca-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sabado', 'Domingo')
    short_name_month = ('Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez')
    name_month = (
    'Janeiro', 'Fevereiro', 'Marco', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro',
    'Dezembro')
    trimestre = ('1º Tri', '2º Tri', '3º Tri', '4º Tri')

    def __init__(self, dt_referencia, nome_dia, nome_mes, nome_mes_ano, numero_ano, numero_dia,
                 numero_mes, numero_mes_ano, trimestre, feriado, numero_dia_semana, numero_semana):
        """ 01/01/2019 """
        self.dt_referencia = dt_referencia
        """ Segunda-Feira """
        self.nome_dia = nome_dia
        """ Janeiro """
        self.nome_mes = nome_mes
        """ Jan/2019 """
        self.nome_mes_ano = nome_mes_ano
        """ 2019 """
        self.numero_ano = numero_ano
        """ 02 """
        self.numero_dia = numero_dia
        """ 01 """
        self.numero_mes = numero_mes
        """ 01/2019 """
        self.numero_mes_ano = numero_mes_ano
        """ 1º Tri/19 """
        self.trimestre = trimestre
        """ S ou N """
        self.feriado = feriado
        """  01 """
        self.numero_dia_semana = numero_dia_semana
        """ 05 """
        self.numero_semana = numero_semana

    def __str__(self):
        return f'{self.dt_referencia} - {self.nome_dia} - {self.nome_mes} - {self.nome_mes_ano}' \
               f'- {self.numero_ano} - {self.numero_dia} - {self.numero_mes} - {self.numero_mes_ano}' \
               f' - {self.trimestre} - {self.feriado} - {self.numero_dia_semana} - {self.numero_semana}'

    def to_tuple(self):
        return (self.dt_referencia, self.nome_dia, self.nome_mes, self.nome_mes_ano, self.numero_ano, self.numero_dia,
                self.numero_mes, self.numero_mes_ano, self.trimestre, self.feriado, self.numero_dia_semana,
                self.numero_semana)


def gera_datas():
    datas = []
    for ano in range(year_begin, year_end + 1):
        for mes in range(1, 13):
            for dia in range(1, 32):
                if mes == 2 and dia > 28:
                    if is_bissexto(ano):
                        if dia > 29:
                            break
                    else:
                        break
                if mes in (4, 6, 9, 11) and dia > 30:
                    break

                da = date(ano, month=mes, day=dia)
                calen = Calendario(da.strftime('%d/%m/%Y'),
                                   Calendario.weeks_days[da.weekday()],
                                   Calendario.name_month[da.month - 1],
                                   f'{Calendario.short_name_month[da.month - 1]}/{da.year}',
                                   da.year,
                                   int('{:02d}'.format(da.day)),
                                   int('{:02d}'.format(da.month)),
                                   '{:02d}/{}'.format(da.month, da.year),
                                   '{}/{}'.format(Calendario.trimestre[trimestre(da.month)], da.strftime("%y")),
                                   'N',
                                   dia_semana(da.weekday()),
                                   int(da.strftime("%V"))
                                   )
                datas.append(calen.to_tuple())
    return datas


def dia_semana(n):
    if n == 6:
        return 1
    else:
        return n + 2


def trimestre(mes):
    if mes in (1, 2, 3):
        return 0
    elif mes in (4, 5, 6):
        return 1
    elif mes in (7, 8, 9):
        return 2
    else:
        return 3


def popular_tabela(conexao, calendario):
    if conexao and calendario:
        cursor = conexao.cursor()
        cursor.executemany("""insert into hcv_calendario(DT_REFERENCIA,NOME_DIA,NOME_MES,NOME_MES_ANO,NUMERO_ANO,NUMERO_DIA,NUMERO_MES,NUMERO_MES_ANO, TRIMESTRE, FERIADO, NUMERO_DIA_SEMANA, NUMERO_SEMANA) 
                       values (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12)""", calendario)
    else:
        print("Erro com a conexão!")


def is_bissexto(ano):
    return ano % 4 == 0 and ano % 100 != 0 or ano % 400 == 0


# TODO separar em outro arquivo
class Feriado:
    def __init__(self, nome: str, tipo: str, data):
        self.nome = nome
        self.data = data
        self.tipo = tipo

    def __str__(self):
        return f'{self.nome} na data {self.data} do tipo {self.tipo}'

    def __repr__(self):
        return f'{self.nome} na data {self.data} do tipo {self.tipo}'


def busca_feriados(ano, url=URL, token=TOKEN, ibge=CODIGO_CIDADE):
    # preparacao
    payload = {"ano": ano, "ibge": ibge, "token": token}
    try:
        response = get(url, params=payload)
        if response.status_code == 200:
            return [Feriado(fer['name'], fer['type_code'], fer['date']) for fer in response.json()]

    except Exception as err:
        return f"Algum erro ao buscar os feriados!{err}"


def apresentacao(feriados):
    return '\n'.join(feriado.__str__() for feriado in feriados if feriado.tipo == '4')


if __name__ == "__main__":
    # 'usuario/senha@nomeDaAcessoTNS'
    # STRING_CONEXAO = "usuario/senha@nomeDaAcessoTNS"
    # conn = get_con(STRING_CONEXAO)
    # datas = gera_datas()
    # popular_tabela(conn, datas)

    feriados = busca_feriados("2021")

    print(apresentacao(feriados))
