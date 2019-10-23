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

import urllib.parse
import urllib.request

ENDPOINT_DATABASE_PATH = "http://localhost:9001"
ENDPOINT_GET_MOVIE = "/movie"


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

        print(endpoint_get_movie_path)
        response = urllib.request.urlopen(endpoint_get_movie_path).read()  # TODO see the read byte response
        print(response)
        print(type(response))
        # TODO: handle the case response is empty
        dispatcher.utter_message("Recommended movies are:" + response.decode())
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
        return ["year"]

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
        dispatcher.utter_template("utter_movie_match_language_result", tracker)
        return []


class ActionMatchLanguageSearchMovie(Action):

    def name(self):
        # type: () -> Text
        return "action_match_language_search_movie"

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
        if tracker.get_slot('year') is not None:
            dispatcher.utter_template("utter_movie_match_year_result", tracker)
        if tracker.get_slot('genre') is not None:
            dispatcher.utter_template("utter_movie_match_genre_result", tracker)
        if tracker.get_slot('language') is not None:
            dispatcher.utter_template("utter_movie_match_language_result", tracker)
        if tracker.get_slot('year_start') is not None:
            dispatcher.utter_template("utter_movie_match_year_start_result", tracker)
        if tracker.get_slot('year_end') is not None:
            dispatcher.utter_template("utter_movie_match_year_end_result", tracker)
        if tracker.get_slot('rating') is not None:
            dispatcher.utter_template("utter_movie_match_rating_result", tracker)

        call_endpoint_get_movie(tracker, dispatcher)


# TODO: this is level 2
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
    # TODO
    def name(self):
        # type: () -> Text
        return "action_match_rating_search_movie"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        call_endpoint_get_movie(tracker, dispatcher)


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
