import requests


class IdAPIService:
    BASE_URL = "http://127.0.0.1:8001"

    def extract(self, image_path: str) -> dict:
        url = f"{self.BASE_URL}/extract-id/"

        try:
            with open(image_path, "rb") as file:
                files = {
                    "file": (image_path, file, "application/octet-stream")
                }

                response = requests.post(url, files=files)

            if response.status_code == 200:
                return response.json() or {}

            elif response.status_code == 422:
                raise Exception(f"Validation Error: {response.json()}")

            else:
                raise Exception(
                    f"ID API Error: {response.status_code} - {response.text}"
                )

        except Exception as e:
            raise Exception(f"Failed calling ID API: {str(e)}")