import requests
import xmltodict
import time
from app.config import PANORAMA_URL
from app.keyvault_client import get_secret


class PanoramaClient:

    def __init__(self):
        self.api_key = None

    def _generate_api_key(self):
        username = get_secret("panorama-username")
        password = get_secret("panorama-password")

        params = {
            "type": "keygen",
            "user": username,
            "password": password
        }

        response = requests.get(f"{PANORAMA_URL}/api/", params=params, verify=True)
        data = xmltodict.parse(response.text)

        return data["response"]["result"]["key"]

    def _get_api_key(self):
        if not self.api_key:
            self.api_key = self._generate_api_key()
        return self.api_key

    def _request(self, params):
        try:
            params["key"] = self._get_api_key()

            response = requests.get(
                f"{PANORAMA_URL}/api/",
                params=params,
                verify=True
            )

            return xmltodict.parse(response.text)

        except Exception:
            # retry once with new key
            self.api_key = self._generate_api_key()
            params["key"] = self.api_key

            response = requests.get(
                f"{PANORAMA_URL}/api/",
                params=params,
                verify=True
            )

            return xmltodict.parse(response.text)

    def submit_log_query(self, query: str, log_type="traffic"):
        params = {
            "type": "log",
            "log-type": log_type,
            "query": query
        }

        data = self._request(params)
        return data["response"]["result"]["job"]

    def wait_for_job(self, job_id: str, timeout=30):
        start = time.time()

        while time.time() - start < timeout:
            params = {
                "type": "log",
                "action": "get",
                "job-id": job_id
            }

            data = self._request(params)

            status = data["response"]["result"]["job"]["status"]

            if status == "FIN":
                return data

            time.sleep(2)

        raise TimeoutError("Panorama job timeout")

    def query_logs(self, query: str, log_type="traffic"):
        job_id = self.submit_log_query(query, log_type)
        result = self.wait_for_job(job_id)

        return result["response"]["result"]["log"]["logs"]
