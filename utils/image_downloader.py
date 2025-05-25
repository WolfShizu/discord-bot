import requests

class ImageDownloader:
    @staticmethod
    def get_image(url):
        """
        Baixa uma imagem de uma URL e retorna ela como uma string de bytes
        Args:
            url (str): URL da imagem para download
        Returns:
            bytes: A imagem como uma string de bytes
        Raises:
            requests.exceptions.RequestException: Caso a url ou a requisição tenha alguma falha 
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Falha ao baixar a imagem: {str(e)}")