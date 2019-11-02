# Movie Chatbot

##  Introduction
This conversational AI chatbot was created to simplify the search for a movie to watch. Its capabilities are divided into three parts:
1 ) retrieve movie(s) that match one or more criteria (director name, actor name, year, genre and rating);
2) answer general questions about movies (as for example: who was the director? when was released? who were the actors? what is the genre?);
3) suggest movies based on their characteristics (for example: what films do you have from last year that include space travel and aliens ? In this case, movies with “space travel and aliens” will be retrieved).

These three capabilities will be further explained.


## Project Structure
- cmudatabase
- imdbdatabase
- kaggledatabase
- movie_chatbot
- Utility functions: InvertedIndexUtils.py and TextProcessingUtils.py
- MovieSearchAPI.py 

### Database description 

- imdbdatabase: can be obtained through https://www.imdb.com/interfaces/. This dataset contains title information, rating, and people information.

- kaggledatabase: can be obtained through https://www.kaggle.com/iarunava/imdb-movie-reviews-dataset
This dataset contains 50,000 reviews movie reviews along with their associated binary sentiment polarity labels. A negative review has a score <= 4 out of 10, and a positive review has a score >= 7 out of 10. The review is associated with the IMDB URL, where the movie IMDB ID can be directly obtained.

- cmudatabase: can be obtained through http://www.cs.cmu.edu/~ark/personas/ contains plot summaries of 42,306 movies extracted from Wikipedia, as well as, movie attributes if 81,741 movies extracted from Freebase (movie name, release date, genres, etc).

### MovieSearchAPI

For Rasa server to obtain the necessary data, it was decided to isolate the server that performs the necessary queries in the database. Thus, a REST API was created with endpoints that return the required information asked by a user to the bot. For that purpose, Flask, a python web framework was used.

### Rasa description (movie_chatbot)

The machine learning framework used in this project was Rasa (open source).
Rasa has two main modules:

- Rasa NLU (Natural Language Understanding) for understanding user messages, detecting Intent and Entity in the message. For example: “Who was the director of the godfather?”
So the intent is “get_director_by_movie_title” and the entity is “movie_title”. The training data is written to nlu.md file. This file is composed by the intents and few ways users might express them, custom entities with lookup tables and synonyms.

Rasa NLU has a number of different components, which together make a pipeline. This pipeline defines the flow of data processing and intent classification and entity extraction. (config.yml)

TODO FOTO AND DESCRIBE CONPONENTS

OBS: There are to entities extractor on the pipeline. The CRFEntityExtractor component can learn custom entities in any language, given some training data. Duckling lets you extract common entities like dates, amounts of money, distances, and others in a number of languages. It has the capability of turning expressions like “from last year” into actual datetime objects. 

- Rasa Core is a dialogue management engine with the purpose of holding conversations and deciding what to do next. For that, it uses a machine learning model trained on example conversations to decide what to do next  (trigger Rasa Action Server), using a probabilistic model like LSTM neural network. For dialogue training, Rasa has four main components:
Domain (domain.yml): This file lists all the intents, entities, actions, templates and slots.
Stories (stories.md):  define the interaction/paths between the user and the chatbot. When an intent is detected by Rasa NLU the actions that should be taken by the bot are described in this file.
Example: FOTO
Rasa (Core) creates a probable model of interaction from each story. FOTO?
Like in the example the bot got the intent of getting the director name given the movie title. Until a valid director name is not detected to fill the required slot of the form, the bot will keep asking for a valid one. When it gets it, the bot will continue to the action….
Policies (policy.yml): decide which action to take at every step. At every turn of the conversation, each policy defined will predict the next action with a certain confidence level. The next action is decided by the policy with the highest 
confidence. The FallbackPolicy invokes a fallback action if the requirements nlu_threshold and core_threshold are not met. In this case, the bot will respond with “utter_default”.

Actions (actions.py): has the custom and the form actions defined. In the form action, the bot keeps asking for more details to get all the required entities to fulfil the retrieval. In the custom action, the Movie Search API is invoked via REST API (QueryCore.py) for querying the database to get the information - used to simulate a third party API interaction.

### Setup