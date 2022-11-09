import requests
from bs4 import BeautifulSoup

from web_app.src.dinning_hall import DinningHall


class FoodOptions:
    main_url = "https://nutrition.sa.ucsc.edu/"

    def __init__(self) -> None:
        self.dinning_halls = self.__retrieve_data()

    def get_dh(self, name: str) -> DinningHall:
        return self.dinning_halls[name]

    def __retrieve_data(self) -> dict:
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

        dhs = {}
        for dh_url in dh_urls:
            dinning_hall = DinningHall(dh_url)
            dhs[dinning_hall.name] = dinning_hall

        return dhs

    def __str__(self) -> str:
        result = ""
        for dh in self.dinning_halls.values():
            result += str(dh)
        return result


if __name__ == "__main__":
    fo = FoodOptions()
    print(fo)
