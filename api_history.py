import requests
import time
from datetime import datetime, timedelta

from typing import List
from typing import Any
from dataclasses import dataclass
import json


@dataclass
class Record:
    id: str
    created_at: str
    color: str
    roll: int

    @staticmethod
    def from_dict(obj: Any) -> 'Record':
        _id = str(obj.get("id"))
        _created_at = str(obj.get("created_at"))
        _color = str(obj.get("color"))
        _roll = int(obj.get("roll"))
        return Record(_id, _created_at, _color, _roll)


@dataclass
class Root:
    total_pages: int
    records: List[Record]

    @staticmethod
    def from_dict(obj: Any) -> 'Root':
        _total_pages = int(obj.get("total_pages"))
        _records = [Record.from_dict(y) for y in obj.get("records")]
        return Root(_total_pages, _records)

def resultados():
    cookies = {
        '_gid': 'GA1.2.781127896.1714749072',
        'AMP_MKTG': 'JTdCJTdE',
        '_did': 'web_712234434B09A034',
        'kwai_uuid': '4f8f5347e9db8f1a30e3a0751d616c40',
        '_gcl_au': '1.1.1274132088.1714749077',
        '_fbp': 'fb.1.1714749077202.1498210684',
        'AMP': 'JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjI5NTBlMTNlMy05MDBiLTQwMTQtYWE2Yy0xZDY4MWEzOGVmNzYlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzE0NzQ5MDc0MzA0JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTcxNDc0OTA3NDM5MCUyQyUyMmxhc3RFdmVudElkJTIyJTNBMCU3RA==',
        '_ga_LR2H8FWXB7': 'GS1.1.1714757367.3.1.1714757372.0.0.0',
        '_ga': 'GA1.1.1834781342.1714749072',
    }

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,zh;q=0.5,it;q=0.4,es;q=0.3,ru;q=0.2',
        'device_id': '950e13e3-900b-4014-aa6c-1d681a38ef76',
        'ipcountry': 'BR',
        'priority': 'u=1, i',
        'referer': 'https://jonbet.com/pt/games/double',
        'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'session_id': '1714749074304',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'x-client-language': 'pt',
        'x-client-version': 'v2.280.0',
        'x-kl-kis-ajax-request': 'Ajax_Request',
    }

    response = requests.get('https://jonbet.com/api/roulette_games/history', cookies=cookies, headers=headers)

    if response.status_code == 200:
        data = response.json()  # Converte a resposta em JSON
        
        # Verifica se 'records' está na resposta
        if 'records' in data and isinstance(data['records'], list):
            results = [result['roll'] for result in data['records'] if 'roll' in result]
            created_at_list = [result['created_at'] for result in data['records'] if 'created_at' in result]
            return results, created_at_list
        else:
            print("A chave 'records' não está presente ou não é uma lista:", data)
            return [], []
    else:
        print(f"Erro na requisição: {response.status_code} - {response.text}")
        return [], []

def proximo_minuto_zerado():
    agora = datetime.now()
    # Calcula o próximo horário zerado múltiplo de 10 minutos
    proximo_minuto = (agora.minute // 10 + 1) * 10
    if proximo_minuto >= 60:
        proximo_minuto = 0
        agora += timedelta(hours=1)
    proximo_zerado = agora.replace(minute=proximo_minuto, second=0, microsecond=0)
    return proximo_zerado

resultado_anterior = []
minutos_zerados_roll = []  # Nova lista para armazenar valores de roll com minutos zerados
mensagens_exibidas = set()  # Inicializa a lista para controlar quais mensagens já foram exibidas

while True:
    results, created_at_list = resultados()

    # Contagem de itens na lista
    count = len(results)
    
    if resultado_anterior != results:
        resultado_anterior = results
        print('\nHistórico das últimas 100 casas:', results)
        
        # Filtra os valores de roll com minutos zerados
        novos_minutos_zerados_roll = []
        for i, created_at in enumerate(created_at_list):
            # Converte a string de data/hora em um objeto datetime
            hora = datetime.fromisoformat(created_at[:-1])  # Remove o 'Z'
            hora -= timedelta(hours=3)  # Ajusta para o fuso horário
            if hora.minute % 10 == 0:  # Verifica se os minutos são múltiplos de 10
                roll_value = results[i]
                if roll_value not in minutos_zerados_roll:
                    novos_minutos_zerados_roll.append(roll_value)
                    if novos_minutos_zerados_roll:  # Verifica se a lista não está vazia
                        ultimo_valor = novos_minutos_zerados_roll[-1]  # Obtém o último valor adicionado
                        print(f"Entrar no minuto: {ultimo_valor}")  # Imprime a mensagem concatenada com o último valor
        
        minutos_zerados_roll.extend(novos_minutos_zerados_roll)
        print('Histórico das 10 casas do minuto 0:', minutos_zerados_roll)

        # Obtém a hora do item mais antigo usando 'created_at'
        if count > 0 and created_at_list:
            # O item mais antigo é o primeiro da lista 'created_at_list'
            hora_item_mais_antigo_str = created_at_list[99]
            # Converte a string de data/hora em um objeto datetime
            hora_item_mais_antigo = datetime.fromisoformat(hora_item_mais_antigo_str[:-1])  # Remove o 'Z'
            # Subtrai 3 horas
            hora_item_mais_antigo -= timedelta(hours=3)
            print(f"Horário atual: {hora_item_mais_antigo.strftime('%H:%M:%S')}")

            # Adiciona os minutos correspondentes aos valores de 'roll'
            agora = datetime.now() - timedelta(hours=3)  # Ajusta para o fuso horário
            for roll in results:
                minuto = agora.replace(minute=int(roll))
                if minuto not in mensagens_exibidas:
                    # Exibe a mensagem apenas se for o minuto correspondente
                    if minuto.minute == agora.minute + 1:  # Verifica se é um minuto após
                        if novos_minutos_zerados_roll:  # Verifica se a lista não está vazia
                            ultimo_valor = novos_minutos_zerados_roll[-1]  # Obtém o último valor adicionado
                            print(f"Entrar no minuto: {ultimo_valor}")  # Imprime a mensagem concatenada com o último valor
                        mensagens_exibidas.add(minuto)  # Marca como exibido

        # Imprime o próximo horário zerado
        proximo_zerado = proximo_minuto_zerado()
        print(f"A próxima casa zerada é ás: {proximo_zerado.strftime('%H:%M')}")
        
    time.sleep(2)
