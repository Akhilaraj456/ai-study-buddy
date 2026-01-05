import os
from openai import AzureOpenAI

_client = None

def get_client() -> AzureOpenAI:
    global _client
    if _client is not None:
        return _client

    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION")

    if not endpoint or not api_key or not api_version:
        raise RuntimeError("Missing Azure OpenAI env vars. Check AZURE_OPENAI_ENDPOINT/API_KEY/API_VERSION")

    _client = AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=api_key,
        api_version=api_version,
    )
    return _client


def chat_completion(system: str, user: str, temperature: float = 0.2) -> str:
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    if not deployment:
        raise RuntimeError("Missing AZURE_OPENAI_DEPLOYMENT")

    client = get_client()
    resp = client.chat.completions.create(
        model=deployment,  # Azure uses deployment name here
        temperature=temperature,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )

    return resp.choices[0].message.content or ""
