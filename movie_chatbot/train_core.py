import logging

from rasa.core.policies.fallback import FallbackPolicy
from rasa.core.policies.keras_policy import KerasPolicy
from rasa.core.policies.memoization import MemoizationPolicy
from rasa.core.policies.mapping_policy import MappingPolicy
from rasa.core.policies.form_policy import FormPolicy
from rasa.core.agent import Agent
import asyncio
import get_file_paths

logging.basicConfig(level="CRITICAL")

file_paths = get_file_paths.getFilePaths()


def train_core():
    fallback_policy = FallbackPolicy(core_threshold=0.3, nlu_threshold=0.3) #TODO see this values
    agent = Agent(file_paths['movie_domain_path'],
                  policies=[MemoizationPolicy(), KerasPolicy(), MappingPolicy(), FormPolicy(), fallback_policy])

    loop = asyncio.get_event_loop()
    training_data = loop.run_until_complete(agent.load_data(file_paths['movie_training_files'] + 'stories.md'))

    agent.train(training_data)

    agent.persist(file_paths['movie_model_path'])


train_core()
