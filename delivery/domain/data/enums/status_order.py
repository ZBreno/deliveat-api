from enum import Enum

class StatusChoices(Enum):
    PENDENTE = 'PENDENTE'
    ACEITO = 'ACEITO'
    PRONTO = 'PRONTO'
    ENVIADO = 'ENVIADO'
    CONCLUIDO = 'CONCLUIDO'