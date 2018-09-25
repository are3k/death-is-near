

from requests import get

api_base_url = "https://www.vegvesen.no/nvdb/api/v2/"


def get_json(base_url, endpoint):
    url = f"{base_url}{endpoint}.json"
    return get(url).json()

if __name__ == '__main__':
    data = get_json(api_base_url, "vegobjekter")
    print(data)