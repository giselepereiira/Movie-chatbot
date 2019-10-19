def getFilePaths():
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

    movie_model_path = movie_models_output + movie_model_name + "/"

    return {"movie_project": movie_project,
            "movie_config_path": movie_config_path,
            "movie_training_files": movie_training_files,
            "movie_training_file_nlu": movie_training_file_nlu,
            "movie_training_file_stories": movie_training_file_stories,
            "movie_domain_path": movie_domain_path,
            "movie_models_output": movie_models_output,
            "movie_actions_file": movie_actions_file,
            "movie_endpoints_file": movie_endpoints_file,
            "movie_model_name": movie_model_name,
            "movie_model_path": movie_model_path}
