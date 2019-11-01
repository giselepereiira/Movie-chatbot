import asyncio
import logging

from IPython.display import Image
from IPython.display import display
from rasa.core.agent import Agent
from rasa.core.interpreter import NaturalLanguageInterpreter
from rasa.utils.endpoints import EndpointConfig

logging.basicConfig(level="CRITICAL")

example_project = "Movie-Rasa-Project"
example_config_path = example_project + "\\config.yml"
example_training_files = example_project + "\\data\\"
example_training_file_nlu = example_project + "\\data\\nlu.md"
example_training_file_stories = example_project + "\\data\\stories.md"
example_domain_path = example_project + "\\domain.yml"
example_models_output = example_project + "\\models\\"
example_actions_file = example_project + "\\actions.py"
example_endpoints_file = example_project + "\\endpoints.yml"
example_model_name = "movie_rasa_model"

# example_model_path = "Movie-Rasa-project\\models\\20191101-151805.tar.gz"
example_model_path = example_models_output + example_model_name + "\\"

PORT=5055


# tar = tarfile.open(example_models_output + "20191101-151805" + ".tar.gz", "r:gz")
# tar.extractall(example_models_output + example_model_name)
# tar.close()

#interpreter = Interpreter.load(example_models_output + example_model_name + "/nlu/")


def load_assistant():
    messages = ["Hi! you can chat in this window. Type 'stop' to end the conversation."]
    interpreter = NaturalLanguageInterpreter.create(example_models_output + example_model_name + "\\nlu\\")
    endpoint = EndpointConfig('http://localhost:{}/webhook'.format(PORT))
    agent = Agent.load(example_model_path, interpreter=interpreter, action_endpoint=endpoint)

    print("Your bot is ready to talk! Type your messages here or send 'stop'")
    while True:
        user_message = input()
        if user_message == 'stop':
            break

        loop = asyncio.get_event_loop()
        responses = loop.run_until_complete(agent.handle_text(user_message))
        for response in responses:
            for response_type, value in response.items():
                if response_type == "text":
                    print(value)

                if response_type == "image":
                    image = Image(url=value)
                    display(image)
load_assistant()