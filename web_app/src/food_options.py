import requests
from bs4 import BeautifulSoup

from web_app.src.dinning_hall import DinningHall


class FoodOptions:
    main_url = "https://nutrition.sa.ucsc.edu/"

    def __init__(self) -> None:
        self.dinning_halls = {}
        self.get_dh_data()

    def get_dh(self) -> dict:
        return self.dinning_halls

    def get_dh_data(self) -> None:
        try:
            response = requests.get(self.main_url)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise SystemExit(e)

        html_text = response.text
        soup = BeautifulSoup(html_text, 'html.parser')

        dh_urls = []

        locations = soup.find_all("li", class_="locations")
        for el in locations[:4]:
            line = el.find("a")
            dh_urls.append(self.main_url + line.get('href'))

        for dh_url in dh_urls:
            dinning_hall = DinningHall(dh_url)
            self.dinning_halls[dinning_hall.name] = dinning_hall

    def __str__(self) -> str:
        result = ""
        for dh in self.dinning_halls.values():
            result += str(dh)
        return result


if __name__ == "__main__":
    fo = FoodOptions()
    print(fo)
