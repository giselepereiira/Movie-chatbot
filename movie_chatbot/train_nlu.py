import rasa
from rasa.nlu.model import Metadata, Interpreter
from rasa.nlu.training_data import load_data
from rasa.nlu.model import Trainer
from rasa.nlu import config
import tarfile
import GetFilePaths

files_path = GetFilePaths.getFilePaths()

movie_model_path = rasa.train(files_path['movie_domain_path'], files_path['movie_config_path'],[files_path['movie_training_files']],
files_path['movie_models_output'], fixed_model_name=files_path['movie_model_name'])

tar = tarfile.open(files_path['movie_models_output'] + files_path['movie_model_name'] + ".tar.gz", "r:gz")
tar.extractall(files_path['movie_models_output'] + files_path['movie_model_name'])
tar.close()

interpreter = Interpreter.load(files_path['movie_models_output'] + files_path['movie_model_name'] + "/nlu/")

def train_movie_nlu_model():
    example_training_data = load_data(files_path['movie_training_file_nlu'])

    trainer = Trainer(config.load(files_path['movie_config_path']))

    interpreter = trainer.train(example_training_data)

    model_directory = trainer.persist(files_path['movie_models_output'] + files_path['movie_model_name'], fixed_model_name="nlu")

    return interpreter


train_movie_nlu_model()