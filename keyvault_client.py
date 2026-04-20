
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from app.config import KEYVAULT_URL

credential = DefaultAzureCredential()
client = SecretClient(vault_url=KEYVAULT_URL, credential=credential)


def get_secret(name: str) -> str:
    return client.get_secret(name).value
