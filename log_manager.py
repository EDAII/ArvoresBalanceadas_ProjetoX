# Quantas linhas de log mostrar na tela
MAX_LOG_LINES = 30

# Lista "global" para armazenar as mensagens
_log_messages = []

def add_log(message):
    """ Adiciona uma nova mensagem ao log """
    
    # Imprime no terminal (para ainda termos o log lá, se quisermos)
    print(message) 
    
    # Adiciona na nossa lista
    _log_messages.append(str(message))
    
    # Garante que a lista não cresça para sempre
    # Mantém apenas as últimas MAX_LOG_LINES
    if len(_log_messages) > MAX_LOG_LINES:
        _log_messages.pop(0) # Remove a mensagem mais antiga

def get_messages():
    """ Retorna a lista atual de mensagens de log """
    return _log_messages