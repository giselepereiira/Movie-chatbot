import rasa
from rasa.cli.scaffold import create_initial_project
from rasa.nlu.model import Metadata, Interpreter
from rasa.nlu.training_data import load_data
from rasa.nlu.config import RasaNLUModelConfig
from rasa.nlu.model import Trainer
from rasa.nlu import config
import tarfile

movie_project = "Movie-Rasa-Project"
create_initial_project(movie_project)

movie_config_path = movie_project + "/config.yml"
movie_training_files = movie_project + "/data/"
movie_training_file_nlu = movie_project + "/data/nlu.md"
movie_training_file_stories = movie_project + "/data/stories.md"
movie_domain_path = movie_project + "/domain.yml"
movie_models_output = movie_project + "/models/"
movie_actions_file = movie_project + "/actions.py"
movie_endpoints_file = movie_project + "/endpoints.yml"
movie_model_name = "movie_rasa_model"

movie_model_path = rasa.train(movie_domain_path, movie_config_path, [movie_training_files], movie_models_output, fixed_model_name=movie_model_name)


tar = tarfile.open(movie_models_output + movie_model_name + ".tar.gz", "r:gz")
tar.extractall(movie_models_output + movie_model_name)
tar.close()

interpreter = Interpreter.load(movie_models_output + movie_model_name + "/nlu/")

def train_example_nlu_model():
    example_training_data = load_data(movie_training_file_nlu)

    trainer = Trainer(config.load(movie_config_path))

    interpreter = trainer.train(example_training_data)

    model_directory = trainer.persist(movie_models_output + movie_model_name, fixed_model_name="nlu")

    return interpreter

interpreter = train_example_nlu_model()
print(interpreter.parse("Is there any good ferrari from 2017?")) # Now the intent 'car_search' is detected