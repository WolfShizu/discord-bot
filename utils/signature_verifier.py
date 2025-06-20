import os

from nacl.signing import VerifyKey

class SignatureVerifier:
    @staticmethod
    def verify_signature(event):
        """
        Verifica se a assinatura está correta
        Arguments:
            event(dict): Payload da requisição
        """
        PUBLIC_KEY = os.getenv("PUBLIC_KEY") 
        raw_body = event.get("rawBody")

        auth_sig = event['params']['header'].get('x-signature-ed25519')
        auth_ts  = event['params']['header'].get('x-signature-timestamp')
        
        message = auth_ts.encode() + raw_body.encode()
        verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))
        try:
            verify_key.verify(message, bytes.fromhex(auth_sig))
        except Exception as e:
            raise Exception(f"[UNAUTHORIZED] Assinatura de solicitação inválida: {e}")