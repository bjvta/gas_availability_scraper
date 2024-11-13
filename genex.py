import requests
from bs4 import BeautifulSoup

GENEX_PATH = 'https://genex.com.bo/estaciones/?2729_product_cat%5B0%5D=289&2729_filtered=true'

def scrape_gas_stations(url):
    # Fetch the content from the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return []

    gas_stations = []
    soup = BeautifulSoup(response.content, "html.parser")

    # Locate all entries for "Saldos de ESPECIAL +"
    entries = soup.find_all(
        "tr",
        class_="wcpt-row",
    )

    for entry in entries:
        first_data_section = entry.find(
            'td', 
            class_="wcpt-cell wcpt-1706832047"
        ).find('div', class_="wcpt-cell-val")
        second_data_section = entry.find(
            'td', 
            class_="wcpt-cell wcpt-1706812911725"
        ).find('div', class_="wcpt-cell-val")

        # Name
        station_name_div = first_data_section.find(
            'div',
        ).find('div', class_="wcpt-custom-field")
        station_name = station_name_div.get_text(strip=True) if station_name_div else "N/A"
        # Adress
        station_address_div = first_data_section.find(
            'div',
            class_="wcpt-1706813609825"
        ).find('div')
        station_address = station_address_div.get_text(strip=True) if station_address_div else "N/A"
        # Last Update
        last_update_div = first_data_section.find(
            'div',
            class_="wcpt-1706914115869"
        ).find('div')
        last_update = last_update_div.get_text(strip=True) if last_update_div else "N/A"
        # Have Gas
        have_gas_div = second_data_section.find(
            'div',
        ).find('span', class_="wcpt-text")
        have_gas = have_gas_div.get_text(strip=True) if have_gas_div else "N/A"

        gas_station_data = {
            "Gas Station": station_name,
            "Address": station_address,
            "Last Update": last_update,
            "Have Gas": have_gas,
        }
        gas_stations.append(gas_station_data)


    return gas_stations

gas_station_data = scrape_gas_stations(GENEX_PATH)
for station in gas_station_data:
    print("Gas Station:", station["Gas Station"])
    print("Availability:", station["Have Gas"])
    print("Last measurement:", station["Last Update"])
    print("Location:", station["Address"])
    print("-" * 40)