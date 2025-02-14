from flask import Flask
import requests

app = Flask(__name__)

BASE_URL = "https://sidebar.stract.to/api/"
HEADERS = {"Authorization": "ProcessoSeletivoStract2025"}
ESSENTIAL_COLUMNS = ["Platform", "Account Name"]

def round_floats(value, decimals=3):
    if isinstance(value, float):
        return round(value, decimals)
    return value

def generate_html_table(data, headers):
    table = "<table border='1'><tr>"
    for header in headers:
        table += f"<th>{header}</th>"
    table += "</tr>"
    for row in data:
        table += "<tr>"
        for item in row:
            item = round_floats(item)
            table += f"<td>{item}</td>"
        table += "</tr>"
    table += "</table>"
    return table

def fetch_all_data(endpoint, params=None):
    all_data = []
    page = 1
    while True:
        if params is None:
            params = {}
        params["page"] = page

        url = BASE_URL + endpoint
        try:
            response = requests.get(url, headers=HEADERS, params=params)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from {endpoint}: {e}")
            break

        if "pagination" not in data:
            all_data.extend(data.get("platforms", data.get("accounts", data.get("fields", data.get("insights", [])))))
            break
        else:
            all_data.extend(data.get("platforms", data.get("accounts", data.get("fields", data.get("insights", [])))))

            if data["pagination"]["current"] >= data["pagination"]["total"]:
                break

            page += 1

    return all_data

def generate_html_table(data, headers):
    table = "<table border='1'><tr>"
    for header in headers:
        table += f"<th>{header}</th>"
    table += "</tr>"
    for row in data:
        table += "<tr>"
        for item in row:
            table += f"<td>{item}</td>"
        table += "</tr>"
    table += "</table>"
    return table

def get_platform_mapping():
    platforms_data = fetch_all_data("platforms")
    if not platforms_data:
        return None
    return {platform["value"]: platform["text"] for platform in platforms_data}

@app.route("/")
def root():
    return """
    <h1>Bem-vindo à API</h1>
    <p>Name: Pedro Henrique Fernandes de Oliveira</p>
    <p>Email: pedrohfo@gmail.com</p>
    <p>LinkedIn: <a href="https://www.linkedin.com/in/pedrohfo7/">Meu LinkedIn</a></p>
    """

@app.route("/<platform>")
def platform_ads(platform):
    platform_mapping = get_platform_mapping()
    if not platform_mapping:
        return "Failed to fetch platform mapping", 500

    accounts_data = fetch_all_data(f"accounts?platform={platform}")
    if not accounts_data:
        return "Failed to fetch accounts data", 500

    fields_data = fetch_all_data(f"fields?platform={platform}")
    if not fields_data:
        return "Failed to fetch fields data", 500

    headers = ["Platform", "Account"] + [field["text"] for field in fields_data]
    rows = []

    for account in accounts_data:
        params = {
            "platform": platform,
            "account": account["id"],
            "token": account["token"],
            "fields": ",".join([field["value"] for field in fields_data])
        }
        insights_data = fetch_all_data("insights", params=params)
        if insights_data:
            for insight in insights_data:
                row = [platform_mapping.get(platform, platform), account["name"]] + [insight.get(field["value"], "") for field in fields_data]
                rows.append(row)

    table = generate_html_table(rows, headers)
    return f"<h1>{platform_mapping.get(platform, platform)} Ads</h1>{table}"

@app.route("/<platform>/resumo")
def platform_summary(platform):
    platform_mapping = get_platform_mapping()
    if not platform_mapping:
        return "Failed to fetch platform mapping", 500

    accounts_data = fetch_all_data(f"accounts?platform={platform}")
    if not accounts_data:
        return "Failed to fetch accounts data", 500

    fields_data = fetch_all_data(f"fields?platform={platform}")
    if not fields_data:
        return "Failed to fetch fields data", 500

    headers = ["Platform", "Account Name"] + [field["text"] for field in fields_data]
    rows = []

    for account in accounts_data:
        params = {
            "platform": platform,
            "account": account["id"],
            "token": account["token"],
            "fields": ",".join([field["value"] for field in fields_data])
        }
        insights_data = fetch_all_data("insights", params=params)
        if insights_data:
            aggregated_insights = {field["value"]: 0 for field in fields_data}
            for insight in insights_data:
                for field in fields_data:
                    field_value = insight.get(field["value"])
                    if field_value is not None:
                        try:
                            if isinstance(field_value, str):
                                if "." in field_value:
                                    field_value = float(field_value)
                                else:
                                    field_value = int(field_value)
                            aggregated_insights[field["value"]] += field_value
                        except (ValueError, TypeError):
                            pass

            rounded_insights = {
                k: round_floats(v) if v != 0 else ""
                for k, v in aggregated_insights.items()
            }

            row = [platform_mapping.get(platform, platform), account["name"]] + [
                rounded_insights[field["value"]] for field in fields_data
            ]
            rows.append(row)

    table = generate_html_table(rows, headers)
    return f"<h1>{platform_mapping.get(platform, platform)} Summary</h1>{table}"

@app.route("/geral")
def general_ads():
    platform_mapping = get_platform_mapping()
    if not platform_mapping:
        return "Failed to fetch platform mapping", 500

    platforms_data = fetch_all_data("platforms")
    if not platforms_data:
        return "Failed to fetch platforms data", 500

    headers = ["Platform", "Account Name"]
    fields_set = set()

    for platform in platforms_data:
        fields_data = fetch_all_data(f"fields?platform={platform['value']}")
        if fields_data:
            fields_set.update([field["text"] for field in fields_data])

    headers.extend(fields_set)

    rows = []

    for platform in platforms_data:
        accounts_data = fetch_all_data(f"accounts?platform={platform['value']}")
        if accounts_data:
            for account in accounts_data:
                fields_data = fetch_all_data(f"fields?platform={platform['value']}")
                if fields_data:
                    params = {
                        "platform": platform["value"],
                        "account": account["id"],
                        "token": account["token"],
                        "fields": ",".join([field["value"] for field in fields_data])
                    }
                    insights_data = fetch_all_data("insights", params=params)
                    if insights_data:
                        for insight in insights_data:
                            row = {
                                "Platform": platform_mapping.get(platform["value"], platform["value"]),
                                "Account Name": account["name"]
                            }
                            for field in fields_data:
                                row[field["text"]] = insight.get(field["value"], "")

                            if "Cost Per Click" in headers and "Cost Per Click" not in row:
                                clicks = insight.get("clicks", 0)
                                spend = insight.get("cost", 0)
                                if (clicks != 0) and (spend != 0):
                                    row["Cost Per Click"] = round_floats(spend / clicks)
                                else:
                                    row["Cost Per Click"] = ""

                            rows.append([row.get(header, "") for header in headers])

    table = generate_html_table(rows, headers)
    return f"<h1>General Ads</h1>{table}"

@app.route("/geral/resumo")
def general_ads_summary():
    platform_mapping = get_platform_mapping()
    if not platform_mapping:
        return "Failed to fetch platform mapping", 500

    platforms_data = fetch_all_data("platforms")
    if not platforms_data:
        return "Failed to fetch platforms data", 500

    headers = ["Platform"]
    fields_set = set()

    for platform in platforms_data:
        fields_data = fetch_all_data(f"fields?platform={platform['value']}")
        if fields_data:
            fields_set.update([field["text"] for field in fields_data])

    headers.extend(fields_set)

    platform_aggregates = {}

    platforms_without_cpc = set()
    for platform in platforms_data:
        platform_value = platform["value"]
        fields_data = fetch_all_data(f"fields?platform={platform_value}")
        if fields_data:
            field_names = [field["text"] for field in fields_data]
            if "Cost Per Click" not in field_names:
                platforms_without_cpc.add(platform_value)

    for platform in platforms_data:
        platform_value = platform["value"]
        platform_name = platform_mapping.get(platform_value, platform_value)

        if platform_name not in platform_aggregates:
            platform_aggregates[platform_name] = {field: 0 for field in fields_set}

        accounts_data = fetch_all_data(f"accounts?platform={platform_value}")
        if accounts_data:
            for account in accounts_data:
                fields_data = fetch_all_data(f"fields?platform={platform_value}")
                if fields_data:
                    params = {
                        "platform": platform_value,
                        "account": account["id"],
                        "token": account["token"],
                        "fields": ",".join([field["value"] for field in fields_data])
                    }
                    insights_data = fetch_all_data("insights", params=params)
                    if insights_data:
                        for insight in insights_data:
                            if platform_value in platforms_without_cpc:
                                clicks = insight.get("clicks", 0)
                                spend = insight.get("cost", 0)
                                if clicks != 0 and spend != 0:
                                    cpc = round_floats(spend / clicks)
                                    platform_aggregates[platform_name]["Cost Per Click"] += cpc

                            for field in fields_data:
                                field_value = insight.get(field["value"])
                                if field_value is not None:
                                    try:
                                        if isinstance(field_value, str):
                                            if "." in field_value:
                                                field_value = float(field_value)
                                            else:
                                                field_value = int(field_value)
                                        platform_aggregates[platform_name][field["text"]] += field_value
                                    except (ValueError, TypeError):
                                        pass

    rows = []
    for platform_name, aggregated_data in platform_aggregates.items():
        row = [platform_name]
        for field in fields_set:
            value = aggregated_data.get(field, "")
            if value == 0:
                value = ""
            row.append(round_floats(value) if isinstance(value, (int, float)) else value)
        rows.append(row)

    table = generate_html_table(rows, headers)
    return f"<h1>General Ads Summary</h1>{table}"

if __name__ == "__main__":
    app.run(debug=True)