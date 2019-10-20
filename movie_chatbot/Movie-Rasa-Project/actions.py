# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List, Union, Optional

from rasa_sdk import Tracker, Action
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction, REQUESTED_SLOT

class MovieSearchForm(FormAction):

    def name(self):
        # type: () -> Text
        print("i'm on the MovieSearchForm!")
        return "movie_search_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        print("i'm on the MovieSearchForm! required_slots")
        return ["director"]

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        # utter submit template
        dispatcher.utter_template("utter_movie_search_result", tracker)
        print("i'm on the MovieSearchForm! submit")
        return [SlotSet("director", None)]

class ActionSearchMovie(Action):
#TODO
    def name(self):
        # type: () -> Text
        return "action_search_movie"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print( "i'm on the action_search_movie!")

        # import os
        # cwd = os.getcwd()
        #
        # print(cwd)
        #
        # cars_dataset = self._get_dataset()
        #
        # year_of_manufacture = tracker.get_slot("year_of_manufacture")
        # brand_name = tracker.get_slot("brand_name")
        #
        # cars_according_to_year = cars_dataset.loc[cars_dataset['year'] == year_of_manufacture]
        # cars_filtered = cars_according_to_year.loc[cars_according_to_year["brand"] == brand_name]

    #     cars_brand_model = (
    #                 cars_filtered['year'] + ' ' + cars_filtered['brand'] + ' ' + cars_filtered['model']).tolist()
    #
    #     if len(cars_brand_model) > 0:
    #         dispatcher.utter_message("Cars with brand {} manufactured in the year {} found:\\n-"
    #                                  .format(brand_name, year_of_manufacture) + "\\n-".join(cars_brand_model))
    #     else:
    #         dispatcher.utter_message("No cars with brand {} manufactured in the year {} were found"
    #                                  .format(brand_name, year_of_manufacture))
    #
    #     return [SlotSet("year_of_manufacture", None), SlotSet("brand_name", None)]
    #
    # def _get_dataset(self):
    #     with open('../cars.csv') as csv_file:
    #         csv_reader = csv.reader(csv_file, delimiter=',')
    #         column_names = csv_reader.__next__()
    #         indices_dictionary = {}
    #
    #         max_size = 0
    #
    #         dataset_rows = []
    #         for row in csv_reader:
    #             car_brand = row[1]
    #             year_of_manufacture = row[0]
    #             car_model = row[2]
    #
    #             dataset_rows.append(
    #                 {"year": year_of_manufacture, "brand": car_brand.lower(), "model": car_model.lower()})
    #
    #         cars_dataset = pd.DataFrame(dataset_rows)
    #     return cars_dataset
    #

class MovieSearchFormActor(FormAction):

    def name(self):
        # type: () -> Text
        return "movie_search_actor_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["actor"]

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        # utter submit template
        dispatcher.utter_template("utter_movie_search_actor_result", tracker)
        return [SlotSet("actor", None)]

class ActionSearchMovieActor(Action):
#TODO
    def name(self):
        # type: () -> Text
        return "action_search_movie_actor"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print( "i'm on the action_search_movie_actor!")