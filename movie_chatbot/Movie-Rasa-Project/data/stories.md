## happy path
* greet
  - utter_greet
* mood_great
  - utter_happy

## sad path 1
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* affirm
  - utter_happy

## sad path 2
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* deny
  - utter_goodbye

## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot
    
## search movie by director
* movie_match_director
    - movie_match_director_form
    - slot{"director": "quentin tarantino"}
    - form{"name":"movie_match_director_form"}
    - form{"name": null}
    - action_match_director_search_movie
    
## search movie by actor
* movie_match_actor
    - movie_match_actor_form
    - slot{"actor": "tom cruise"}
    - form{"name":"movie_match_actor_form"}
    - form{"name": null}
    - action_match_actor_search_movie
    
## search movie by year
* movie_match_year
    - movie_match_year_form
    - slot{"year_start": "1995"}
    - form{"name":"movie_match_year_form"}
    - form{"name": null}
    - action_match_year_search_movie
    
## search movie by genre
* movie_match_genre
    - movie_match_genre_form
    - slot{"genre": "comedy"}
    - form{"name":"movie_match_genre_form"}
    - form{"name": null}
    - action_match_genre_search_movie

 ## search movie by several criteria  
* movie_match_several_criteria
   - action_match_several_criteria_search_movie

 ## search movie with rating
* movie_match_rating
   - movie_match_rating_form
   - slot{"rating": "top 4"}
   - form{"name":"movie_match_rating_form"}
   - form{"name": null}
   - action_match_rating_search_movie

 ## search director with movie title
* get_director_by_movie_title
   - get_director_by_movie_title_form
   - slot{"movie_title": "joker"}
   - form{"name":"get_director_by_movie_title_form"}
   - form{"name": null}
   - action_get_director_by_movie_title

 ## search actor with movie title
* get_actor_by_movie_title
   - get_actor_by_movie_title_form
   - slot{"movie_title": "joker"}
   - form{"name":"get_actor_by_movie_title_form"}
   - form{"name": null}
   - action_get_actor_by_movie_title
   
## search year with movie title
* get_year_by_movie_title
   - get_year_by_movie_title_form
   - slot{"movie_title": "joker"}
   - form{"name":"get_year_by_movie_title_form"}
   - form{"name": null}
   - action_get_year_by_movie_title

## search genre with movie title
* get_genre_by_movie_title
   - get_genre_by_movie_title_form
   - slot{"movie_title": "joker"}
   - form{"name":"get_genre_by_movie_title_form"}
   - form{"name": null}
   - action_get_genre_by_movie_title
   
## search rating with movie title
* get_rating_by_movie_title
   - get_rating_by_movie_title_form
   - slot{"movie_title": "joker"}
   - form{"name":"get_rating_by_movie_title_form"}
   - form{"name": null}
   - action_get_rating_by_movie_title
   
   
##search for movies based on its attributes
* get_movie_attributes
    - action_get_movie_based_attribute