import time
from datetime import date, timedelta
from requests import get

import locale

from models import Feriado, Calendario

locale.setlocale(locale.LC_TIME, "pt_BR")

CODIGO_CIDADE = "4106902"

TOKEN = "d2FsaWNlbi5kYWxhenVhbmFAY3J1enZlcm1lbGhhcHIuY29tLmJyJmhhc2g9OTcwOTY4NDk"  # Todo pegar de arquivo .env

URL = "https://api.calendario.com.br/?json=true"

INICIO = 2000
FIM = 2050


def gera_datas(ano_inicio=INICIO, ano_fim=FIM):
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
    # Preparacao
    inicio = date(year=ano_inicio, month=1, day=1)
    fim = date(year=ano_fim, month=12, day=31)
    datas = []

    while inicio <= fim:
        print(inicio.strftime("%a, %d %b %B %Y %H:%M:%S"))
        data = Calendario(inicio.strftime('%d/%m/%Y'),
                          inicio.strftime('%A'),
                          inicio.strftime('%B'),
                          f'{inicio.strftime("%b")}/{inicio.year}',
                          inicio.year,
                          int('{:02d}'.format(inicio.day)),
                          int('{:02d}'.format(inicio.month)),
                          '{:02d}/{}'.format(inicio.month, inicio.year),
                          f'{(inicio.month -1) // 3 +1}º Tri/{inicio.strftime("%y")}',
                          'N',
                          dia_semana(inicio.weekday()),
                          int(inicio.strftime("%V"))
                          )
        datas.append(data)
        inicio += timedelta(days=1)

    return datas


def dia_semana(n):
    if n == 6:
        return 1
    else:
        return n + 2


def popular_tabela(conexao, calendario):
    if conexao and calendario:
        cursor = conexao.cursor()
        cursor.executemany("""insert into hcv_calendario(DT_REFERENCIA,NOME_DIA,NOME_MES,NOME_MES_ANO,NUMERO_ANO,NUMERO_DIA,NUMERO_MES,NUMERO_MES_ANO, TRIMESTRE, FERIADO, NUMERO_DIA_SEMANA, NUMERO_SEMANA) 
                       values (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12)""", calendario)
    else:
        print("Erro com a conexão!")


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

    datas = gera_datas()
    # popular_tabela(conn, datas)
    feriados = busca_feriados("2021")

    print(datas)
    print(apresentacao(feriados))
