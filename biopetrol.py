import requests
from bs4 import BeautifulSoup

def scrape_gas_stations(url):
    # Fetch the content from the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")

    gas_stations = []

    # Locate all entries for "Saldos de ESPECIAL +"
    entries = soup.find_all(
        "div",
        class_="col-11 col-xl-5 col-lg-5 col-md-5 col-sm-7 btn-bio-app rounded my-2 mx-auto p-0 lineh text-bio-app",
    )

    for entry in entries:
        title_div = entry.find(
            "div",
            class_="col-12 m-0 p-0 text-center font-18 font-weight-bold bg-oscuro-1 py-2 mb-1 rounded-top",
        )
        title = title_div.get_text(strip=True) if title_div else "N/A"

        # Find "Existencia en Litros"
        litros_label = entry.find("div", string="Existencia en Litros:")
        litros_value = (
            litros_label.find_next("div").get_text(strip=True)
            if litros_label
            else "N/A"
        )

        hora_label = entry.find("div", string="Hora Medición:")
        hora_value = (
            hora_label.find_next("div").get_text(strip=True) if hora_label else "N/A"
        )

        location_div = entry.find("div", class_="px-1 col-12")
        location = location_div.get_text(strip=True) if location_div else "N/A"

        gas_station_data = {
            "Gas Station": title,
            "Availability": litros_value,
            "Last measurement": hora_value,
            "Location": location,
        }

        gas_stations.append(gas_station_data)

    return gas_stations

url = (
    "http://ec2-3-22-240-207.us-east-2.compute.amazonaws.com/guiasaldos/main/donde/134"
)
gas_station_data = scrape_gas_stations(url)
for station in gas_station_data:
    print("Gas Station:", station["Gas Station"])
    print("Availability:", station["Availability"])
    print("Last measurement:", station["Last measurement"])
    print("Location:", station["Location"])
    print("-" * 40)
