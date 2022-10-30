import requests
from bs4 import BeautifulSoup


class DinningHall:
    def __init__(self, url: str) -> None:
        self.name = ""
        self.foods = {
            'Breakfast': [],
            'Lunch': [],
            'Dinner': [],
            'Late Night': []
        }
        self.retrive_data(url)

    def get_name(self) -> str:
        return self.name

    def get_meal(self, meal: str) -> list[str]:
        if meal in self.foods:
            return self.foods[meal]
        else:
            raise KeyError(f"meal type {meal} not available")

    def retrive_data(self, url: str) -> None:
        cookies = {
            'WebInaCartLocation': '',
            'WebInaCartDates': '',
            'WebInaCartMeals': '',
            'WebInaCartRecipes': '',
            'WebInaCartQtys': '',
        }

        try:
            response = requests.get(url, cookies=cookies)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise SystemExit(e)

        html_text = response.text
        soup = BeautifulSoup(html_text, 'html.parser')

        name = soup.find_all("div", class_="headlocation")
        if name:
            self.name = name[0].get_text()

        mt_index = -1
        for element in soup.find_all("div", {"class": ["shortmenurecipes", "shortmenumeals"]}):
            meal_times = list(self.foods.keys())
            if element.get_text() in meal_times:
                mt_index += 1
            else:
                self.foods[meal_times[mt_index]].append(
                    element.get_text().strip())
