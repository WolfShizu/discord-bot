from utils.signature_verifier import SignatureVerifier
from commands.commands import CommandMap

def lambda_handler(event, context):

    SignatureVerifier.verify_signature(event)

    payload = event.get('body-json')

    if payload.get("type") == 1:
        return {
            "type": 1
        }

    commands_map = CommandMap.get_commands()

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
