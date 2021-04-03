
class Feriado:
    def __init__(self, nome: str, tipo: str, data):
        self.nome = nome
        self.data = data
        self.tipo = tipo

    def __str__(self):
        return f'{self.nome} na data {self.data} do tipo {self.tipo}'

    def __repr__(self):
        return f'{self.nome} na data {self.data} do tipo {self.tipo}'


class Calendario():

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
