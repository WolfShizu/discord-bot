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
        from utils.image_downloader import ImageDownloader
        from aws.aws_rekognition import AWSRekognition
        
        attachment_id = next(iter(self.payload["data"]["resolved"]["attachments"]))
        attachment = self.payload["data"]["resolved"]["attachments"][attachment_id]
        image_url = attachment["url"]
        image_bytes = ImageDownloader.get_image(image_url)

        labels = AWSRekognition.detect_labels(image_bytes)

        names = [name["Name"] for name in labels["Labels"]]
        confidences = [confidence["Confidence"] for confidence in labels["Labels"]]

        content = [
            f"Tenho ``{confidence:.2f}%`` de certeza da imagem conter um ``{name}``"
            for name, confidence in zip(names, confidences)
            ]

        content = "\n".join(content)
        content = content + f"\n[imagem]({attachment["url"]})"

        return {
            "type": 4,
            "data": {
                "content": content
            } 
        }