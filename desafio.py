import requests

url = "https://sidebar.stract.to/api/insights?platform=meta_ads&account=1&token=cf76cf576fc567fc56fc5c6f5cf67fc6&fields=clicks,spend,cpc"
headers = {"Authorization": "ProcessoSeletivoStract2025"}
params = {"page": 2}

try:
    response = requests.get(url, headers=headers, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        try:
            data = response.json()  # Parse JSON
            print(data)
        except requests.exceptions.JSONDecodeError:
            print("Error: Response is not valid JSON.")
            print("Response content:\n", response.text)
    else:
        print(f"Error: Request failed with status code {response.status_code}")
        print("Response content:\n", response.text)

except requests.exceptions.RequestException as e:
    print(f"Error: Request failed - {e}")