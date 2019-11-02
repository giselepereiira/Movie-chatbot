import asyncio
import logging

from rasa.core.agent import Agent
from rasa.core.interpreter import NaturalLanguageInterpreter
from rasa.utils.endpoints import EndpointConfig

logging.basicConfig(level="CRITICAL")

# Project paths
project = "Movie-Rasa-Project"
movie_config_path = project + "\\config.yml"
movie_training_files = project + "\\data\\"
movie_training_file_nlu = project + "\\data\\nlu.md"
movie_training_file_stories = project + "\\data\\stories.md"
movie_domain_path = project + "\\domain.yml"
movie_models_output = project + "\\models\\"
movie_actions_file = project + "\\actions.py"
movie_endpoints_file = project + "\\endpoints.yml"
movie_model_name = "movie_rasa_model"

example_model_path = movie_models_output + movie_model_name + "\\"

PORT_ACTIONS = 5055


# Uncomment this is you trained a new model
# name_of_new_model="dummy-name"
# tar = tarfile.open(movie_models_output + name_of_new_model + ".tar.gz", "r:gz")
# tar.extractall(movie_models_output + movie_model_name)
# tar.close()


def load_assistant():
    interpreter = NaturalLanguageInterpreter.create(movie_models_output + movie_model_name + "\\nlu\\")
    endpoint = EndpointConfig('http://localhost:{}/webhook'.format(PORT_ACTIONS))
    agent = Agent.load(example_model_path, interpreter=interpreter, action_endpoint=endpoint)

    print("Your bot is ready to talk! Type your messages here or send 'stop'")
    while True:
        user_message = input("---> ")
        if user_message == 'stop':
            break

        loop = asyncio.get_event_loop()
        responses = loop.run_until_complete(agent.handle_text(user_message))
        for response in responses:
            for response_type, value in response.items():
                if response_type == "text":
                    print(value)


load_assistant()
