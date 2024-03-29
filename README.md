# Movie Chatbot

## Table of Contents
1. [Introduction](#introduction)
2. [Architecture](#architecture)
3. [Project Structure](#project-structure)
    - [Database description and setup](#database-description-and-setup)
    - [MovieSearchAPI](#moviesearchapi)
    - [Rasa description (movie_chatbot)](#rasa-description-movie_chatbot)
4. [Setup](#setup)
5. [Sources](#sources)

##  Introduction 
This conversational AI chatbot was created to simplify the search for a movie to watch. Its capabilities are divided into three parts:

1. Retrieve movie(s) that match one or more criteria (director name, actor name, year, genre and rating);

2. Answer general questions about movies (as for example: who was the director? when was released? who were the actors? what is the genre?);

3. Suggest movies based on their characteristics (for example: what films do you have from last year that include space travel and aliens ? In this case, movies with “space travel and aliens” will be retrieved).

These three capabilities are further explained [here](Approach.md).

##  Architecture  

![Architecture](images/ArchitectureDiagram.png)

## Project Structure
- cmudatabase
- imdbdatabase
- kaggledatabase
- movie_chatbot
- utils
- api


### Database description and setup

- folder **imdbdatabase**:  The IMDB dataset contains title information, rating, and people information. 

To setup this dataset, download the files available at https://www.imdb.com/interfaces/ and extract them in a new folder named “dataset” on the root of the project. 

Install PostgreSQL (https://www.postgresql.org/download/) and create a new database of your choice. After, it is needed to define the database configurations on variable db_config on `DatabaseConstants.py`. To import the data, just run `IMToDB.py` (Disclaimer: this process takes a long time).

- folder **kaggledatabase**: The kaggle dataset contains 50,000 movie reviews along with their associated binary sentiment polarity labels. A negative review has a score <= 4 out of 10, and a positive review has a score >= 7 out of 10. The review is associated with the IMDB URL, where the movie IMDB ID can be directly obtained. 

To setup this dataset, download the files available at https://www.kaggle.com/iarunava/imdb-movie-reviews-dataset and extract them to kaggledatabase folder. Run `ImporterKaggle.py` and change the variable path. Then, run `CreateIndexKaggle.py` for positive reviews and negative reviews.

- folder **cmudatabase**: The CMU database contains plot summaries of 42,306 movies extracted from Wikipedia, as well as, movie attributes if 81,741 movies extracted from Freebase (movie name, release date, genres, etc).

To setup this dataset, download the files available at http://www.cs.cmu.edu/~ark/personas/ and extract them on cmudatabase folder. Following, run `ImporterCmu.py` and `CreateIndexCmu.py`.



### MovieSearchAPI (folder api)

For Rasa server to obtain the necessary data, it was decided to isolate the server that performs the necessary queries in the database. Thus, a REST API was created with endpoints that return the required information asked by a user to the bot. 

For that purpose, Flask, a python web framework was used.

![APIDiagram](images/APIDiagram.png)

### Rasa description (folder movie_chatbot)

The machine learning framework used in this project was Rasa (open source).
Rasa has two main modules:

- *Rasa NLU* (Natural Language Understanding) for understanding user messages, detecting Intent and Entity in the message. For example: “Who was the director of the godfather?”
So the intent is “get_director_by_movie_title” and the entity is “movie_title”. 
The training data is written to `nlu.md` file. This file is composed by the intents and few ways users might express them, custom entities with lookup tables and synonyms.

Rasa NLU has a number of different components, which together make a pipeline. This pipeline defines the flow of data processing and intent classification and entity extraction (`config.yml`).

```yaml
language: en

pipeline:
    - name: SpacyNLP
    - name: SpacyTokenizer
    - name: SpacyFeaturizer
    - name: RegexFeaturizer
    - name: CRFEntityExtractor
    - name: DucklingHTTPExtractor
      url: http://localhost:8000
      dimensions:
      - time
    - name: EntitySynonymMapper
    - name: SklearnIntentClassifier
```

OBS: There are two entities extractor on the pipeline. The `CRFEntityExtractor` component can learn custom entities in any language, given some training data. `DucklingHTTPExtractor` lets you extract common entities like dates, amounts of money, distances, and others in a number of languages. It has the capability of turning expressions like “from last year” into actual datetime objects. 

- *Rasa Core* is a dialogue management engine with the purpose of holding conversations and deciding what to do next. For that, it uses a machine learning model trained on example conversations to decide what to do next (trigger Rasa Action Server), using a probabilistic model like LSTM neural network. 
For dialogue training, Rasa has four main components:

    * Domain (`domain.yml`): This file lists all the intents, entities, actions, templates and slots.
    
    * Stories (`stories.md`):  define the interaction/paths between the user and the chatbot. When an intent is detected by Rasa NLU, the following actions that should be taken by the bot are described in this file.
    
    ![Diagram](images/StoryExample.jpg)

    Like in the above example, the bot got the intent of getting the director name given the movie title. Until a valid director name is not detected to fill the required slot of the form, the bot will keep asking for a valid one. When it gets it, the bot will continue to the action.
   
    * Policies (`policy.yml`): decide which action to take at every step. At every turn of the conversation, each policy defined will predict the next action with a certain confidence level. The next action is decided by the policy with the highest 
confidence. The `FallbackPolicy` invokes a fallback action if the requirements nlu_threshold and core_threshold are not met. In this case, the bot will respond with “utter_default”.

    * Actions (`actions.py`): has the custom and the form actions defined. In the form action, the bot keeps asking for more details to get all the required entities to fulfil the retrieval. In the custom action, the Movie Search API is invoked via REST API (`MovieSearchAPI.py`) for querying the database to get the information - used to simulate a third party API interaction.


## Setup
1. First, it is needed to install python 3, create and activate a virtual environment. Using venv:

```python
python -m venv <DIR>
source <DIR>/bin/activate
```

2. Once the environment is active, at the same directory, clone this repository.

3. Install the list of requirements specified in `movie-chatbot-requirements.txt`

```python
pip install -r movie-chatbot-requirements.txt
```
(Note: In case you are working on windows, make sure you have installed the Visual c++ build tool. This is a requirement for Rasa installation).

4. After you need to install Duckling for Rasa NLU entity extraction (`DucklingHTTPExtractor`). 
To use this component you need to run a duckling server. The easiest option is to spin up a docker container using `docker run -p 8000:8000 rasa/duckling`. Please obtain docker container on https://hub.docker.com/r/rasa/duckling. 

Great! Now you have everything ready to search movies!

5. Run `MovieSearchAPI.py`. The default host is 127.0.0.1 and the port is 9001. 

6. Run the action server in port 5055.
```python python -m rasa_sdk --actions actions --port 5055```
 If you want to change the port 5055, change `endpoint.yml`.

7. To interact with the chatbot run `load_assitant.py`

OR

To use Rasa assistant, run
```python
rasa x
```
The server will run on  http://localhost:5002/

For exposing your local web server, please install ngrok and run 
```
ngrok http 5002
```
Now, you have no reason not to choose the best movie!

## Sources
1. [Flask](https://www.fullstackpython.com/flask.html)
2. [Rasa](https://rasa.com/)
3. [Rasa X](https://rasa.com/docs/rasa-x/)
4. [Build a Conversational Chatbot with Rasa Stack and Python](https://medium.com/@itsromiljain/build-a-conversational-chatbot-with-rasa-stack-and-python-rasa-nlu-b79dfbe59491)

