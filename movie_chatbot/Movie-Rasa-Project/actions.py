# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

import json
import urllib.parse
import urllib.request
from typing import Any, Text, Dict, List

from rasa_sdk import Tracker, Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction

ENDPOINT_DATABASE_PATH = "http://localhost:9001"
ENDPOINT_GET_MOVIE = "/movie"
ENDPOINT_GET_MOVIE_INFO = "/movieInfo"

def call_endpoint_get_movie(tracker, dispatcher):
    """
    Method to invoke endpoints that returns the movie titles that match the entities detected on the user interaction
    :param tracker: Tracker
    :param dispatcher: Dispatcher
    """
    endpoint_get_movie_path = ENDPOINT_DATABASE_PATH + ENDPOINT_GET_MOVIE
    filter_endpoint = []

    for key, value in tracker.slots.items():
        if value is not None:
            filter_endpoint.append((key, value))

    if len(filter_endpoint) >= 1:
        for idx, val in enumerate(filter_endpoint):
            parsed_query_parameter = val[0] + "=" + urllib.parse.quote(val[1])
            if idx == 0:
                endpoint_get_movie_path = endpoint_get_movie_path + "?" + parsed_query_parameter
            else:
                endpoint_get_movie_path = endpoint_get_movie_path + "&" + parsed_query_parameter

        response = urllib.request.urlopen(endpoint_get_movie_path)
        response_json = json.loads(response.read().decode('utf-8'))

        if not response_json:
            # case the response is empty
            dispatcher.utter_message("No movies found")
        else:
            dispatcher.utter_message("Recommended movies are:")
            for idx, result in enumerate(response_json):
                dispatcher.utter_message(str(idx+1) + ". " + result[0])
    else:
        dispatcher.utter_message("No entity was detected. Please reformulate your search.")


class MovieMatchDirectorForm(FormAction):

    def name(self):
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
        dispatcher.utter_template("utter_movie_match_director_result", tracker)
        return []


class ActionMatchDirectorSearchMovie(Action):

    def name(self):
        # type: () -> Text
        return "action_match_director_search_movie"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        call_endpoint_get_movie(tracker, dispatcher)


class MovieMatchActorForm(FormAction):

    def name(self):
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
        dispatcher.utter_template("utter_movie_match_actor_result", tracker)
        return []


class ActionMatchActorSearchMovie(Action):

    def name(self):
        return "action_match_actor_search_movie"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        call_endpoint_get_movie(tracker, dispatcher)


class MovieMatchYearForm(FormAction):

    def name(self):
        # type: () -> Text
        return "movie_match_year_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["year_start"]

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        # utter submit template
        dispatcher.utter_template("utter_movie_match_year_result", tracker)
        return []


class ActionMatchYearSearchMovie(Action):

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
        dispatcher.utter_template("utter_movie_match_genre_result", tracker)
        return []


class ActionMatchGenreSearchMovie(Action):

    def name(self):
        # type: () -> Text
        return "action_match_genre_search_movie"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        call_endpoint_get_movie(tracker, dispatcher)


class ActionMatchSeveralCriteriaSearchMovie(Action):

    def name(self):
        # type: () -> Text
        return "action_match_several_criteria_search_movie"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print(tracker.slots)

        # These messages are for the user knowing what the chatbot is looking for
        if tracker.get_slot('director') is not None:
            dispatcher.utter_template("utter_movie_match_director_result", tracker)
        if tracker.get_slot('actor') is not None:
            dispatcher.utter_template("utter_movie_match_actor_result", tracker)
        if tracker.get_slot('genre') is not None:
            dispatcher.utter_template("utter_movie_match_genre_result", tracker)
        if tracker.get_slot('year_start') is not None:
            dispatcher.utter_template("utter_movie_match_year_start_result", tracker)
        if tracker.get_slot('year_end') is not None:
            dispatcher.utter_template("utter_movie_match_year_end_result", tracker)
        if tracker.get_slot('rating') is not None:
            dispatcher.utter_template("utter_movie_match_rating_result", tracker)

        call_endpoint_get_movie(tracker, dispatcher)


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

        return []


class ActionMatchRatingSearchMovie(Action):
    def name(self):
        # type: () -> Text
        return "action_match_rating_search_movie"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        call_endpoint_get_movie(tracker, dispatcher)


# This is level 2

def call_endpoint_get_movie_info(tracker):
    endpoint_path = ENDPOINT_DATABASE_PATH + ENDPOINT_GET_MOVIE_INFO

    value_movie_title = tracker.get_slot('movie_title')

    if value_movie_title is not None:

        endpoint_path = endpoint_path + "?movie_title=" + urllib.parse.quote(value_movie_title)
        response = urllib.request.urlopen(endpoint_path)
        response_json = json.loads(response.read().decode('utf-8'))

        if not response_json:
            # case the response is empty
            return "MovieTitleNotFound"
        else:
            return response_json
    else:
        return "NoMovieTitleDetected"


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
        return []


class ActionGetDirectorByMovieTitle(Action):
    def name(self):
        # type: () -> Text
        return "action_get_director_by_movie_title"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        response = call_endpoint_get_movie_info(tracker)
        if response == "MovieTitleNotFound":
            dispatcher.utter_message("This movie title was not found")
        elif response == "NoMovieTitleDetected":
            dispatcher.utter_message("No movie title detected. Please reformulate your search.")
        else:
            # TODO: response get
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
        return []


class ActionGetActorByMovieTitle(Action):

    def name(self):
        # type: () -> Text
        return "action_get_actor_by_movie_title"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        response = call_endpoint_get_movie_info(tracker)
        if response == "MovieTitleNotFound":
            dispatcher.utter_message("This movie title was not found")
        elif response == "NoMovieTitleDetected":
            dispatcher.utter_message("No movie title detected. Please reformulate your search.")
        else:
            # TODO: response get
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
        return []


class ActionGetYearByMovieTitle(Action):

    def name(self):
        # type: () -> Text
        return "action_get_year_by_movie_title"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        response = call_endpoint_get_movie_info(tracker)
        if response == "MovieTitleNotFound":
            dispatcher.utter_message("This movie title was not found")
        elif response == "NoMovieTitleDetected":
            dispatcher.utter_message("No movie title detected. Please reformulate your search.")
        else:
            # TODO: response get
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
        return []


class ActionGetGenreByMovieTitle(Action):

    def name(self):
        # type: () -> Text
        return "action_get_genre_by_movie_title"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        response = call_endpoint_get_movie_info(tracker)
        if response == "MovieTitleNotFound":
            dispatcher.utter_message("This movie title was not found")
        elif response == "NoMovieTitleDetected":
            dispatcher.utter_message("No movie title detected. Please reformulate your search.")
        else:
            # TODO: response get
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
        return []


class ActionGetLanguageByMovieTitle(Action):

    def name(self):
        # type: () -> Text
        return "action_get_language_by_movie_title"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        response = call_endpoint_get_movie_info(tracker)
        if response == "MovieTitleNotFound":
            dispatcher.utter_message("This movie title was not found")
        elif response == "NoMovieTitleDetected":
            dispatcher.utter_message("No movie title detected. Please reformulate your search.")
        else:
            # TODO: response get
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
        return []


class ActionGetRatingByMovieTitle(Action):

    def name(self):
        # type: () -> Text
        return "action_get_rating_by_movie_title"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        response = call_endpoint_get_movie_info(tracker)
        if response == "MovieTitleNotFound":
            dispatcher.utter_message("This movie title was not found")
        elif response == "NoMovieTitleDetected":
            dispatcher.utter_message("No movie title detected. Please reformulate your search.")
        else:
            # TODO: response get
            dispatcher.utter_message("Rating: Dummy rating")


# This is level 3

def call_endpoint_level3(tracker, dispatcher):
    """
    Method to invoke endpoints that returns the movie titles that match the entities detected on the user interaction
    :param tracker: Tracker
    :param dispatcher: Dispatcher
    """
    endpoint_get_movie_path = ENDPOINT_DATABASE_PATH + "/level3"
    filter_endpoint = []

    time_duckling_value = tracker.get_slot("time")
    movie_characteristic_value = tracker.get_slot("movie_characteristic")
    if time_duckling_value is not None:
        year_to_search = time_duckling_value['from'][0:4]
        filter_endpoint.append(("year_start", year_to_search))
    if movie_characteristic_value is not None:
        filter_endpoint.append(('movie_characteristic', movie_characteristic_value))
    # for key, value in tracker.slots.items():
    #   if value is not None:
    #      filter_endpoint.append((key, value))

    if len(filter_endpoint) >= 1:
        for idx, val in enumerate(filter_endpoint):
            parsed_query_parameter = val[0] + "=" + urllib.parse.quote(val[1])
            if idx == 0:
                endpoint_get_movie_path = endpoint_get_movie_path + "?" + parsed_query_parameter
            else:
                endpoint_get_movie_path = endpoint_get_movie_path + "&" + parsed_query_parameter

        print(endpoint_get_movie_path)
        response = urllib.request.urlopen(endpoint_get_movie_path)
        response_json = json.loads(response.read().decode('utf-8'))

        if not response_json:
            # case the response is empty
            dispatcher.utter_message("No movies found")
        else:
            dispatcher.utter_message("Recommended movies are:")
            for idx, result in enumerate(response_json):
                dispatcher.utter_message(str(idx + 1) + ". " + result)
    else:
        dispatcher.utter_message("No entity was detected. Please reformulate your search.")

class ActionDummyLevel3Test(Action):

    def name(self):
        # type: () -> Text
        return "action_dummy_level_3_test"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        time_duckling_value = tracker.get_slot("time")
        movie_characteristic_value = tracker.get_slot("movie_characteristic")

        if time_duckling_value is not None:
            dispatcher.utter_message("duckling detected year:" + time_duckling_value['from'])
            # granularity that matters is only year in that case
            year_to_search = time_duckling_value['from'][0:4]  # example: '2018-01-01T00:00:00.000-08:00'
            print(year_to_search)
        if movie_characteristic_value is not None:
            print(movie_characteristic_value)

            call_endpoint_level3(tracker, dispatcher)
