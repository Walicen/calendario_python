import time
from datetime import date
import cx_Oracle as oracle

#'usuario/senha@nomeDaAcessoTNS'
STRING_CONEXAO = "'usuario/senha@nomeDaAcessoTNS'"

conn = oracle.connect('STRING_CONEXAO')
conn.autocommit = True
year_begin = 2000
year_end = 2050


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

    weeks_days = ('Domingo', 'Segunda-feira', 'Terca-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sabado')
    short_name_month = ('JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ')
    name_month = ('JANEIRO', 'FEVEREIRO', 'MARCO', 'ABRIL', 'MAIO', 'JUNHO', 'JULHO', 'AGOSTO', 'SETEMBRO', 'OUTUBRO', 'NOVEMBRO', 'DEZEMBRO')
    
    def __init__(self, dt_referencia, nome_dia, nome_mes, nome_mes_ano, numero_ano, numero_dia, numero_mes, numero_mes_ano):
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

    def __str__(self):
        return f'{self.dt_referencia} - {self.nome_dia} - {self.nome_mes} - {self.nome_mes_ano} - {self.numero_ano} - {self.numero_dia} - {self.numero_mes} - {self.numero_mes_ano}'

    
    def to_tuple(self):
        return (self.dt_referencia, self.nome_dia, self.nome_mes, self.nome_mes_ano, self.numero_ano, self.numero_dia, self.numero_mes, self.numero_mes_ano)


def gera_datas():
    datas = []
    for ano in range(year_begin, year_end+1):
        for mes in range(1,13):
            for dia in range(1,32):
                if mes == 2 and dia > 28:
                    if is_bissexto(ano):
                        if dia > 29:
                            break
                    else:
                        break
                if mes in (4,6,9,11) and dia > 30:
                    break
                               
                da = date(ano,month=mes, day=dia)
                calen = Calendario(da.strftime('%d/%m/%Y'), 
                                   Calendario.weeks_days[da.weekday()],
                                   Calendario.name_month[da.month-1],
                                   f'{Calendario.short_name_month[da.month-1]}/{da.year}',
                                   da.year,
                                   int('{:02d}'.format(da.day)),
                                   int('{:02d}'.format(da.month)),
                                   '{:02d}/{}'.format(da.month,da.year)
                                   )
                datas.append(calen.to_tuple())
    return datas
               


def popular_tabela(conexao, calendario):
    cursor = conexao.cursor()
    
    query = ("insert into hcv_calendario(DT_REFERENCIA,NOME_DIA,NOME_MES,NOME_MES_ANO,NUMERO_ANO,NUMERO_DIA,NUMERO_MES,NUMERO_MES_ANO)"
             "values (:1, :2, :3, :4, :5, :6, :7, :8)")
    print(query)
    cursor.executemany("insert into hcv_calendario(DT_REFERENCIA,NOME_DIA,NOME_MES,NOME_MES_ANO,NUMERO_ANO,NUMERO_DIA,NUMERO_MES,NUMERO_MES_ANO) " \
                       "values (:1, :2, :3, :4, :5, :6, :7, :8)", calendario)
    
    
    
def is_bissexto(ano):
    return ano % 4 == 0 and ano % 100 != 0 or ano % 400 == 0


if __name__ == "__main__":
    datas = gera_datas()
    popular_tabela(conn, datas)
    
    
    
 
