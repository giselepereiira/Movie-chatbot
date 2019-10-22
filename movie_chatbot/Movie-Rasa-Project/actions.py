# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Tracker, Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction

import urllib.request


def call_endpoint_get_movie(tracker, dispatcher):
    """
    Method to invoke endpoints that returns the movie titles that match the entities detected on the user interaction
    :param tracker: Tracker
    :param dispatcher: Dispatcher
    """
    endpoint = "http://localhost:9001/movie"
    filter_endpoint = []

    for key, value in tracker.slots.items():
        if value is not None:
            filter_endpoint.append(key + "=" + value)

    if len(filter_endpoint) >= 1:
        for idx, val in enumerate(filter_endpoint):
            if idx == 0:
                endpoint = endpoint + "?" + val
            else:
                endpoint = endpoint + "&" + val

        response = urllib.request.urlopen(endpoint).read()
        # TODO: handle the case response is empty
        dispatcher.utter_message("Recommended movies are:" + response.decode())

    else:
        print("No criteria found print") #TODO: pass to utter message


class MovieMatchDirectorForm(FormAction):

    def name(self):
        # type: () -> Text
        return "movie_match_director_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["director"]

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        # utter submit template
        dispatcher.utter_template("utter_movie_match_director_result", tracker)
        return []  # [SlotSet("director", None)]


class ActionMatchDirectorSearchMovie(Action):
    # TODO
    def name(self):
        # type: () -> Text
        return "action_match_director_search_movie"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("Recommended movie: The avengers")

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


class MovieMatchActorForm(FormAction):

    def name(self):
        # type: () -> Text
        return "movie_match_actor_form"

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
        dispatcher.utter_template("utter_movie_match_actor_result", tracker)
        return []  # [SlotSet("actor", None)]


class ActionMatchActorSearchMovie(Action):
    # TODO
    def name(self):
        # type: () -> Text
        return "action_match_actor_search_movie"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("Recommended movie: The avengers")


class MovieMatchYearForm(FormAction):

    def name(self):
        # type: () -> Text
        return "movie_match_year_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["year"]

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        # utter submit template
        dispatcher.utter_template("utter_movie_match_year_result", tracker)
        return []  # [SlotSet("year", None)]


class ActionMatchYearSearchMovie(Action):
    # TODO
    def name(self):
        # type: () -> Text
        return "action_match_year_search_movie"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        call_endpoint_get_movie(tracker, dispatcher)


class MovieMatchGenreForm(FormAction):

    def name(self):
        # type: () -> Text
        return "movie_match_genre_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["genre"]

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        # utter submit template
        dispatcher.utter_template("utter_movie_match_genre_result", tracker)
        return []  # [SlotSet("genre", None)]


class ActionMatchGenreSearchMovie(Action):
    # TODO
    def name(self):
        # type: () -> Text
        return "action_match_genre_search_movie"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("Recommended movie: The avengers")


class MovieMatchLanguageForm(FormAction):

    def name(self):
        # type: () -> Text
        return "movie_match_language_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["language"]

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        # utter submit template
        dispatcher.utter_template("utter_movie_match_language_result", tracker)
        return []  # [SlotSet("language", None)]


class ActionMatchLanguageSearchMovie(Action):
    # TODO
    def name(self):
        # type: () -> Text
        return "action_match_language_search_movie"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("Recommended movie: The avengers")


class MovieMatchSeveralCriteriaForm(FormAction):

    def name(self):
        # type: () -> Text
        return "movie_match_several_criteria_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        print(tracker.slots)
        list_available_slots = list()
        for criteria, criteria_value in tracker.slots.items():
            if criteria_value is not None:
                list_available_slots.append(criteria)
        print(list_available_slots)
        return list_available_slots

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        # utter submit template
        dispatcher.utter_template("utter_movie_match_several_criteria_result", tracker)

        value_actor = tracker.get_slot('actor')
        value_director = tracker.get_slot('director')
        value_language = tracker.get_slot('language')
        value_genre = tracker.get_slot('genre')
        value_year = tracker.get_slot('year')
        value_year_start = tracker.get_slot('year_start')
        value_year_end = tracker.get_slot('year_end')

        if tracker.get_slot('actor') is not None:
            dispatcher.utter_template("utter_movie_match_actor_result", tracker)

        if tracker.get_slot('director') is not None:
            dispatcher.utter_template("utter_movie_match_director_result", tracker)

        if tracker.get_slot('language') is not None:
            dispatcher.utter_template("utter_movie_match_language_result", tracker)

        if tracker.get_slot('genre') is not None:
            dispatcher.utter_template("utter_movie_match_genre_result", tracker)

        if tracker.get_slot('year') is not None:
            dispatcher.utter_template("utter_movie_match_year_result", tracker)

        if tracker.get_slot('year_start') is not None:
            dispatcher.utter_template("utter_movie_match_year_start_result", tracker)

        if tracker.get_slot('year_end') is not None:
            dispatcher.utter_template("utter_movie_match_year_end_result", tracker)

        return []  # [SlotSet("language", value_language), SlotSet("actor", value_actor), SlotSet("director", value_director),
        # SlotSet("genre", value_genre), SlotSet("year", value_year),
        # SlotSet("year_start", value_year_start), SlotSet("year_end", value_year_end)]


class ActionMatchSeveralCriteriaSearchMovie(Action):
    # TODO
    def name(self):
        # type: () -> Text
        return "action_match_several_criteria_search_movie"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        value_actor = tracker.get_slot('actor')
        value_director = tracker.get_slot('director')
        value_language = tracker.get_slot('language')
        value_genre = tracker.get_slot('genre')
        value_year = tracker.get_slot('year')

        dispatcher.utter_message("Recommended movie: The avengers")

        # TODO querys


class MovieMatchRatingForm(FormAction):

    def name(self):
        # type: () -> Text
        return "movie_match_rating_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["rating"]

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        # utter submit template
        dispatcher.utter_template("utter_movie_match_several_criteria_result", tracker)

        value_actor = tracker.get_slot('actor')
        value_director = tracker.get_slot('director')
        value_language = tracker.get_slot('language')
        value_genre = tracker.get_slot('genre')
        value_year = tracker.get_slot('year')
        value_year_start = tracker.get_slot('year_start')
        value_year_end = tracker.get_slot('year_end')
        value_rating = tracker.get_slot('rating')

        if tracker.get_slot('actor') is not None:
            dispatcher.utter_template("utter_movie_match_actor_result", tracker)

        if tracker.get_slot('director') is not None:
            dispatcher.utter_template("utter_movie_match_director_result", tracker)

        if tracker.get_slot('language') is not None:
            dispatcher.utter_template("utter_movie_match_language_result", tracker)

        if tracker.get_slot('genre') is not None:
            dispatcher.utter_template("utter_movie_match_genre_result", tracker)

        if tracker.get_slot('year') is not None:
            dispatcher.utter_template("utter_movie_match_year_result", tracker)

        if tracker.get_slot('year_start') is not None:
            dispatcher.utter_template("utter_movie_match_year_start_result", tracker)

        if tracker.get_slot('year_end') is not None:
            dispatcher.utter_template("utter_movie_match_year_end_result", tracker)

        if tracker.get_slot('rating') is not None:
            dispatcher.utter_template("utter_movie_match_rating_result", tracker)

        return []  # [SlotSet("language", value_language), SlotSet("actor", value_actor), SlotSet("director", value_director),
        # SlotSet("genre", value_genre), SlotSet("year", value_year),
        # SlotSet("year_start", value_year_start), SlotSet("year_end", value_year_end),
        # SlotSet("rating", value_rating)]


class ActionMatchRatingSearchMovie(Action):
    # TODO
    def name(self):
        # type: () -> Text
        return "action_match_rating_search_movie"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("Recommended movie: The avengers")

        # TODO querys


class GetDirectorByMovieTitleForm(FormAction):

    def name(self):
        # type: () -> Text
        return "get_director_by_movie_title_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["movie_title"]

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        # utter submit template
        dispatcher.utter_template("utter_get_director_by_movie_title_result", tracker)
        return []  # [SlotSet("director", None)]


class ActionGetDirectorByMovieTitle(Action):
    # TODO
    def name(self):
        # type: () -> Text
        return "action_get_director_by_movie_title"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("Director: Dummy director")


class GetActorByMovieTitleForm(FormAction):

    def name(self):
        # type: () -> Text
        return "get_actor_by_movie_title_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["movie_title"]

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        # utter submit template
        dispatcher.utter_template("utter_get_actor_by_movie_title_result", tracker)
        return []  # [SlotSet("director", None)]


class ActionGetActorByMovieTitle(Action):

    def name(self):
        # type: () -> Text
        return "action_get_actor_by_movie_title"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("Actor: Dummy actor")


class GetYearByMovieTitleForm(FormAction):

    def name(self):
        # type: () -> Text
        return "get_year_by_movie_title_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["movie_title"]

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        # utter submit template
        dispatcher.utter_template("utter_get_year_by_movie_title_result", tracker)
        return []  # [SlotSet("director", None)]


class ActionGetYearByMovieTitle(Action):

    def name(self):
        # type: () -> Text
        return "action_get_year_by_movie_title"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("Year: Dummy year")


class GetGenreByMovieTitleForm(FormAction):

    def name(self):
        # type: () -> Text
        return "get_genre_by_movie_title_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["movie_title"]

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        # utter submit template
        dispatcher.utter_template("utter_get_genre_by_movie_title_result", tracker)
        return []  # [SlotSet("director", None)]


class ActionGetGenreByMovieTitle(Action):

    def name(self):
        # type: () -> Text
        return "action_get_genre_by_movie_title"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("Genre: Dummy genre")


class GetLanguageByMovieTitleForm(FormAction):

    def name(self):
        # type: () -> Text
        return "get_language_by_movie_title_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["movie_title"]

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        # utter submit template
        dispatcher.utter_template("utter_get_language_by_movie_title_result", tracker)
        return []  # [SlotSet("director", None)]


class ActionGetLanguageByMovieTitle(Action):

    def name(self):
        # type: () -> Text
        return "action_get_language_by_movie_title"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("Language: Dummy language")


class GetRatingByMovieTitleForm(FormAction):

    def name(self):
        # type: () -> Text
        return "get_rating_by_movie_title_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["movie_title"]

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        # utter submit template
        dispatcher.utter_template("utter_get_rating_by_movie_title_result", tracker)
        return []  # [SlotSet("director", None)]


class ActionGetRatingByMovieTitle(Action):

    def name(self):
        # type: () -> Text
        return "action_get_rating_by_movie_title"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("Rating: Dummy rating")
