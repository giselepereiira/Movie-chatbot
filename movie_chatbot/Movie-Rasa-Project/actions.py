# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

import json
import urllib.parse
import urllib.request
from socket import timeout
from typing import Any, Text, Dict, List

from rasa.core.constants import (
    DEFAULT_REQUEST_TIMEOUT
)
from rasa_sdk import Tracker, Action
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction

ENDPOINT_DATABASE_PATH = "http://localhost:9001"
ENDPOINT_GET_MOVIE = "/list-movie"
ENDPOINT_GET_MOVIE_INFO = "/movie-info"
ENDPOINT_GET_MOVIE_WITH_ATTRIBUTES = "/movie-with-attribute"


def call_endpoint_get_movie(tracker, dispatcher):
    """
    Method to invoke endpoints that returns the movie titles that match the entities detected on the user interaction
    :param tracker: Tracker
    :param dispatcher: Dispatcher
    """
    endpoint_get_movie_path = ENDPOINT_DATABASE_PATH + ENDPOINT_GET_MOVIE
    filter_endpoint = []

    for key, value in tracker.slots.items():
        if key == 'rating':
            filter_endpoint.append((key, value.replace('top ', '')))

        if value is not None:
            filter_endpoint.append((key, value))

    print(filter_endpoint)

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
        return [SlotSet("director", None)]



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
        return [SlotSet("actor", None)]


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
        return [SlotSet("year_start", None), SlotSet("time", None)]


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
        return [SlotSet("genre", None)]


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

        list_slot_sets = []
        for key, value in tracker.slots.items():
            if value is not None:
                list_slot_sets.append(SlotSet(key, None))

        return list_slot_sets


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
        return [SlotSet("rating", None)]


def call_endpoint_get_movie_info(tracker):
    endpoint_path = ENDPOINT_DATABASE_PATH + ENDPOINT_GET_MOVIE_INFO

    value_movie_title = tracker.get_slot('movie_title')

    if value_movie_title is not None:

        endpoint_path = endpoint_path + "?movie_title=" + urllib.parse.quote(value_movie_title)

        try:
            print(DEFAULT_REQUEST_TIMEOUT)
            response = urllib.request.urlopen(endpoint_path, timeout=DEFAULT_REQUEST_TIMEOUT)
            print(response)
        except timeout:
            print('Timeout')

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
        print(response)
        if response == "MovieTitleNotFound":
            dispatcher.utter_message("This movie title was not found")
        elif response == "NoMovieTitleDetected":
            dispatcher.utter_message("No movie title detected. Please reformulate your search.")
        else:
            for item in response.items():
                dispatcher.utter_message("Movie title: " + item[0])
                if 'directors' in item[1]:
                    if item[1]['directors'] is not None:
                        dispatcher.utter_message("Director(s):")
                        for index, element in enumerate(item[1]['directors']):
                            dispatcher.utter_message(str(index + 1) + ". " + element)
                    else:
                        dispatcher.utter_message("Directors not found")
                else:
                    dispatcher.utter_message("Directors not found")


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
            for item in response.items():
                dispatcher.utter_message("Movie title: " + item[0])
                if 'actors' in item[1]:
                    if item[1]['actors'] is not None:
                        dispatcher.utter_message("Actor(s):")
                        for index, element in enumerate(item[1]['actors']):
                            dispatcher.utter_message(str(index + 1) + ". " + element)
                    else:
                        dispatcher.utter_message("Actors not found")
                else:
                    dispatcher.utter_message("Actors not found")


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
            for item in response.items():
                dispatcher.utter_message("Movie title: " + item[0])
                if 'year_start' in item[1]:
                    if item[1]['year_start'] is not None:
                        dispatcher.utter_message("Year: " + str(item[1]['year_start']))
                    else:
                        dispatcher.utter_message("Year not found")
                else:
                    dispatcher.utter_message("Year not found")


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
            for item in response.items():
                dispatcher.utter_message("Movie title: " + item[0])
                if 'genres' in item[1]:
                    if item[1]['genres'] is not None:
                        dispatcher.utter_message("Genre(s):")
                        for index, element in enumerate(item[1]['genres']):
                            dispatcher.utter_message(str(index + 1) + ". " + element)
                    else:
                        dispatcher.utter_message("Genre not found")
                else:
                    dispatcher.utter_message("Genre not found")


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
            for item in response.items():
                dispatcher.utter_message("Movie title: " + item[0])
                if 'rating' in item[1]:
                    if item[1]['rating'] is not None:
                        dispatcher.utter_message("Rating: " + str(item[1]['rating']))
                    else:
                        dispatcher.utter_message("Rating not found")
                else:
                    dispatcher.utter_message("Rating not found")


def call_endpoint_get_movie_based_on_attributes(tracker, dispatcher):
    endpoint_get_movie_path = ENDPOINT_DATABASE_PATH + ENDPOINT_GET_MOVIE_WITH_ATTRIBUTES
    filter_endpoint = []

    for key, value in tracker.slots.items():
        if key == "time":
            year_start = tracker.get_slot("time")['from'][0:4]
            filter_endpoint.append(("year_start", year_start))
        if value is not None and key != "time":
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
                dispatcher.utter_message(str(idx + 1) + ". " + result)
    else:
        dispatcher.utter_message("No entity was detected. Please reformulate your search.")


class GetMovieBasedAttributeForm(FormAction):

    def name(self):
        # type: () -> Text
        return "get_movie_based_attribute_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["movie_attribute"]

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        return []

class ActionGetMovieBasedAttribute(Action):

    def name(self):
        # type: () -> Text
        return "action_get_movie_based_attribute"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        call_endpoint_get_movie_based_on_attributes(tracker, dispatcher)
