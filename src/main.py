from dining_hall import DinningHall as DH


url = 'https://nutrition.sa.ucsc.edu/shortmenu.aspx?sName=UC+Santa+Cruz+Dining&locationNum=40&locationName=College+Nine%2fJohn+R.+Lewis+Dining+Hall&naFlag=1'

C9 = DH(url)

print(C9.get_name())
print(C9.get_meal("Dinner"))
