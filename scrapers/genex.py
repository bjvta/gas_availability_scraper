from scrapers.base import PumpBaseScraper
from bs4 import BeautifulSoup
import datetime


class GenexPumpScraper(PumpBaseScraper):
    def parse(self):
        self.fetch_content()
        soup = BeautifulSoup(self.page_content, 'html.parser')
        gas_stations = []

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
                "pump_name": self.page_type,
                "station_name": station_name,
                "availability": None,
                "last_measurement": last_update,
                "latlng": None,
                "location_text": station_address,
                "town": None,
                "canton": None,
                "province": "Santa Cruz de la Sierra",
                "department": "Santa Cruz",
                "city": "Santa Cruz",
                "timestamp": datetime.datetime.now().isoformat(),
                "product": "Especial+",
            }
            gas_stations.append(gas_station_data)

        return gas_stations
