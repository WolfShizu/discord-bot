class CommandMap:
    @staticmethod
    def get_commands():
        """
        Gera um mapa de comandos do bot
        Returns:
            dict: chave: comando(str) | valor: Classe do comando (comando acessado com .execute)
        """
        return {
            "hello": HelloCommand,
            "analisar_imagem": ImageAnalyser
        }

class Command:
    """
    Classe base para as outras classes de comandos
    Args:
        payload(dict): Requisição recebida do discord
    Returns:
        dict: subclasses retornam a resposta formatada para ser enviada como resposta ao discord
    """
    def __init__(self, payload):
        self.payload = payload

    def execute(self):
        raise NotImplementedError("Comando não configurado corretamente")

class HelloCommand(Command):
    """
    Comando básico de "olá"
    """
    def execute(self):
        return {
            "type": 4,
            "data": {
                "content": f"Olá {self.payload["member"]["user"]["username"]}!"
            } 
        }
    
class ImageAnalyser(Command):
    def execute(self):
        attachment_id = next(iter(self.payload["data"]["resolved"]["attachments"]))
        attachment = self.payload["data"]["resolved"]["attachments"][attachment_id]

        return {
            "type": 4,
            "data": {
                "content": f"Nome da imagem: {attachment["filename"]}\nurl da imagem: {attachment["url"]}"
            } 
        }