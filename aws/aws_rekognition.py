import boto3

class AWSRekognition:
    @staticmethod
    def detect_labels(image_bytes):
        client = boto3.client("rekognition")

        response = client.detect_labels(
            Image={
                "Bytes": image_bytes
            },
            MaxLabels=10
        )

        return response