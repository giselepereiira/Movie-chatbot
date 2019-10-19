from rasa.core.policies.keras_policy import KerasPolicy
from rasa.core.policies.memoization import MemoizationPolicy
from rasa.core.policies.mapping_policy import MappingPolicy
from rasa.core.agent import Agent
import asyncio
import logging, io, json, warnings
logging.basicConfig(level="CRITICAL")

movie_project = "Movie-Rasa-Project"

movie_config_path = movie_project + "/config.yml"
movie_training_files = movie_project + "/data/"
movie_training_file_nlu = movie_project + "/data/nlu-movies.md"
movie_training_file_stories = movie_project + "/data/stories.md"
movie_domain_path = movie_project + "/domain.yml"
movie_models_output = movie_project + "/models/"
movie_actions_file = movie_project + "/actions.py"
movie_endpoints_file = movie_project + "/endpoints.yml"
movie_model_name = "movie_rasa_model"

def train_core():
    agent = Agent(movie_domain_path, policies=[MemoizationPolicy(), KerasPolicy(), MappingPolicy()])

    loop = asyncio.get_event_loop()
    training_data = loop.run_until_complete(agent.load_data(movie_training_files + 'stories.md'))

    agent.train(training_data)

    agent.persist(movie_models_output + movie_model_name)

train_core()
example_model_path = movie_models_output + movie_model_name + "/"