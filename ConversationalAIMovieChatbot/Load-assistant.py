import asyncio

import IPython
from IPython.display import clear_output, display
from rasa.core.agent import Agent
from rasa.core.interpreter import NaturalLanguageInterpreter
from rasa.utils.endpoints import EndpointConfig
from IPython.display import Image
import time
import logging
import GetFilePaths

logging.basicConfig(level="CRITICAL")

file_paths = GetFilePaths.getFilePaths()

PORT=5055


def load_assistant():
    messages = ["Hi! you can chat in this window. Type 'stop' to end the conversation."]
    interpreter = NaturalLanguageInterpreter.create(file_paths['movie_models_output'] + file_paths['movie_model_name'] + "/nlu/")
    endpoint = EndpointConfig('http://localhost:{}/webhook'.format(PORT))
    agent = Agent.load(file_paths['movie_model_path'], interpreter=interpreter, action_endpoint=endpoint)

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