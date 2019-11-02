## intent:greet
- hey
- hello
- hi
- good morning
- good evening
- hey there

## intent:goodbye
- bye
- goodbye
- see you around
- see you later

## intent:affirm
- yes
- indeed
- of course
- that sounds good
- correct

## intent:deny
- no
- never
- I don't think so
- don't like that
- no way
- not really

## intent:mood_great
- perfect
- very good
- great
- amazing
- wonderful
- I am feeling very good
- I am great
- I'm good

## intent:mood_unhappy
- sad
- very sad
- unhappy
- bad
- very bad
- awful
- terrible
- not very good
- extremely sad
- so sad

## intent:bot_challenge
- are you a bot?
- are you a human?
- am I talking to a bot?
- am I talking to a human?

## intent:movie_match_director 
- what movies were directed by [quentin tarantino](director)?
- what movies were directed by [steven spielberg](director)?
- what movies were directed by [christopher nolan](director)?
- what movies were directed by [charles roven](director)?
- what movies were directed by [martin scorsese](director)?
- what movies were directed by [scott rudin](director)?
- what are the movies by [stanley kubrick](director)?
- what are the movies by [peter jackson](director)?
- what are the movies by [joel silver](director)?
- what is [quentin tarantino](director) known for?
- what did [ridley scott](director) create?


## intent:movie_match_actor
- what movies had the participation of [tom cruise](actor)?
- what movies had the participation of [brad pitt](actor)?
- what movies had the participation of [tom hanks](actor)?
- what movies had the participation of [leonardo dicaprio](actor)?
- what movies had the participation of [morgan freeman](actor)?
- what movies had the participation of [johnny depp](actor)?
- what movies has [christian bale](actor) worked on?
- what movies has [robert de niro](actor) worked on?
- what movies has [matt damon](actor) worked on?


## intent:movie_match_year
- what were the movies made in 2018?
- what were the movies made in 1980?
- what were the movies made in 1995?
- what were the movies made in 1990?
- what were the movies made in 2005?
- what movies have been released in 2018?
- what movies have been released in 1990?
- what movies have been released in 2000?

## intent:movie_match_genre
- tell me [comedy](genre) movies
- tell me [action](genre) movies
- tell me [horror](genre) movies
- give me [comedy](genre) movies
- give me [action](genre) movies
- give me [horror](genre) movies

## intent:movie_match_several_criteria
- tell me [comedy](genre) movies that had the participation of [tom cruise](actor)
- tell me [drama](genre) movies that had the participation of [brad pitt](actor)
- tell me [comedy](genre) movies that were produced between 2018 and 2019
- tell me [horror](genre)  movies that were produced between 1990 and 2002
- tell me [action](genre) movies that were directed by [tony scott](director)
- tell me movies that were directed by [steven spielberg](director) and had [tom cruise](actor) as an actor
- tell me movies that were directed by [tony scott](director) produced between 1990 and 2002

##intent: movie_match_rating
- what were the [top 5](rating) rated movies in 2018?
- what were the [top 2](rating) rated movies in 2019?
- what were the [top 10](rating) rated movies in 1990?

## lookup:actor
data\lookup-tables\actor_names.txt

## lookup:director
data\lookup-tables\director_names.txt

## lookup:genre
data\lookup-tables\genres_list.txt

## synonym:movies
- films

## regex:rating
- top \b[0-9]+\b

## synonym:directed
- leaded
- coordinated
- orchestrated

##synonym:participation
- involvement
- part
- engagement
- contribution

##synonym:made
- released
- filmed
- produced
- created
- formed

##intent:get_director_by_movie_title
- who was the director of [the godfather](movie_title)?
- who was the director of [inception](movie_title)?
- who was the director of [fight club](movie_title)?
- who was the director of [interstellar](movie_title)?
- who was the director of [the matrix](movie_title)?
- who created [top gun](movie_title)?

##intent:get_actor_by_movie_title
- who were the star actors in [the godfather](movie_title)?
- who were the star actors in [star wars](movie_title)?
- who were the star actors in [inception](movie_title)?
- who were the star actors in [interstellar](movie_title)?
- who were the star actors in [the matrix](movie_title)?

##intent:get_year_by_movie_title
- when was released [the godfather](movie_title)?
- when was released [star wars](movie_title)?
- when was released [fight club](movie_title)?
- when was released [interstellar](movie_title)?
- when was released [inception](movie_title)?
- what year did [miss jerry](movie_title) come out?

##intent:get_genre_by_movie_title
- what is the genre of [the godfather](movie_title)?
- what is the genre of [miss jerry](movie_title)?
- what is the genre of [fight club](movie_title)?
- what is the genre of [interstellar](movie_title)?
- what is the genre of [inception](movie_title)?

##intent:get_rating_by_movie_title
- what is the rating of [the godfather](movie_title)?
- what is the rating of [miss jerry](movie_title)?
- what is the rating of [fight club](movie_title)?
- what is the rating of [interstellar](movie_title)?
- what is the rating of [inception](movie_title)?
- what is [the incredibles](movie_title) rated?

##lookup:movie_title
data\lookup-tables\movie_titles.txt


##intent:get_movie_attributes
- do you have any movie from last year with [awesome special effect](movie_attribute)?
- do you have any movie from two years ago with [awesome special effect](movie_attribute)?
- do you have any movie from three years ago with [awesome special effect](movie_attribute)?
- tell me [drama](genre) movie that [people love for the love story](movie_attribute)
- tell me movies that have [incredible landscapes and nature scenes](movie_attribute)
- what films do you have that include [space travel and aliens](movie_attribute)?
- tell me movies that have [awesome special effect](movie_attribute)
- tell me movies that have [cats and dogs](movie_attribute)

##lookup:movie_attribute
- awesome special effect
- people love for the love story
- incredible landscapes and nature scenes
- space travel and aliens
- cats and dogs
- a lot of blood and war
- super hero
- based on a true story