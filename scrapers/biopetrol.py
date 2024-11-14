from scrapers.base import PumpBaseScraper
from bs4 import BeautifulSoup
import datetime

class BiopetrolPumpScraper(PumpBaseScraper):
    def parse(self):
        self.fetch_content()
        soup = BeautifulSoup(self.page_content, 'html.parser')
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
                "pump_name": self.page_type,
                "station_name": title,
                "availability": litros_value,
                "last_measurement": hora_value,
                "latlng": None,
                "location_text": location,
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
