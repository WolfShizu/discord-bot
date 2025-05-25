from utils.signature_verifier import SignatureVerifier
from commands.commands import CommandMap

def lambda_handler(event, context):
    # Verifica a assinatura do payload
    SignatureVerifier.verify_signature(event)

    # Salva o dicionário do payload
    payload = event.get('body-json')

    # Resposta para a requisição PING do discord
    if payload.get("type") == 1:
        return {
            "type": 1
        }
    # Salva o mapa de comandos do bot
    commands_map = CommandMap.get_commands()

    # Verifica se a classe do comando existe
    try:
        command = commands_map.get(payload["data"]["name"])(payload)
    except Exception as e:
        print(e)

        return {
            "type": 4,
            "data": {
                "content": "Comando não encontrado"
            }
        }

    # Executa o comando
    try: 
        return command.execute()
    except Exception as e:
        print(e)

        return {
            "type": 4,
            "data": {
                "content": "Erro ao executar comando"
            }
        }
