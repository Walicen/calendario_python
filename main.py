import time
from datetime import date
import cx_Oracle as oracle

conn = oracle.connect('tasy/redcross@DBTESTE')


'''
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

'''



class Calendario():

    weeks_days = ('Domingo', 'Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado')
    
    def __init__(self, dt_referencia, nome_dia, nome_mes, nome_mes_ano, numero_ano, numero_dia, numero_mes, numero_mes_ano):
        ''' 01/01/2019 '''
        self.dt_referencia = dt_referencia
        ''' Segunda-Feira '''
        self.nome_dia = nome_dia
        ''' Janeiro '''
        self.nome_mes = nome_mes
        ''' Jan/2019 '''
        self.nome_mes_ano = nome_mes_ano
        ''' 2019 '''
        self.numero_ano = numero_ano
        ''' 02 '''
        self.numero_dia = numero_dia
        ''' 01 '''
        self.numero_mes = numero_mes
        ''' 01/2019 '''
        self.numero_mes_ano = numero_mes_ano


def popular_tabela(conexao):
    cursor = conexao.cursor()
    query = ''' insert into hcv_calendario values(); '''
    



if __name__ == "__main__":
    #popular_tabela(conn)
    #print(time.gmtime())
    """ hoje = date.today()
    hoje_formatado = hoje.strftime('%d/%m/%Y')
    print(hoje_formatado)
    print(hoje.day)
    print(hoje.month)
    print(hoje.year)
    print(hoje.weekday()) """

    ano = date(2019, month=1, day=32)
    print(ano.year)

    
