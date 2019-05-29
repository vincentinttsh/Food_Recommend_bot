import logging
import json
import random


logger = logging.getLogger(__name__)

class FOOD_DATABASE:
    def __init__(self) :
        with open('data.json' , 'r') as reader:
            self.food_database = json.loads(reader.read())
        self.all_restaurant = dict()
        for x in self.food_database['restaurant'].keys() :
            for i in range(1, int(self.food_database['restaurant'][x][0]['length']) + 1) :
                self.all_restaurant[self.food_database['restaurant'][x][i]['name']] = self.food_database['restaurant'][x][i]
    def get_main_category(self) :
        category = list()
        for x in self.food_database['restaurant'].keys() :
            category.append([x])
        category.append(['一日一推薦'])
        return category
    def have_this_category(self, category) :
        return True if category in self.food_database['restaurant'].keys() else False
    def have_this_restaurant(self, restaurant) :
        return True if restaurant in self.all_restaurant.keys() else False
    def get_this_restaurant(self, restaurant ) :
        return self.all_restaurant[restaurant]
    def get_rand_restaurant(self, category = 'NULL') :
        if category == 'NULL' :
            return self.all_restaurant[random.choice(list(self.all_restaurant.keys()))]
        else :
            return self.food_database['restaurant'][category][random.randint(1, self.food_database['restaurant'][category][0]['length'])]
    def get_category_restaurant(self, category) :
            temp = list()
            for i in range(1, int(self.food_database['restaurant'][category][0]['length']) + 1):
                temp.append([self.food_database['restaurant'][category][i]['name']])
            temp.append(['一日一推薦-'+category])
            temp.append(['回到主選單'])
            return temp
    