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
- what movies were directed by [ingmar bergman](director)?
- what movies were directed by [marlon brando](director)?
- what movies were directed by [james cagney](director)?
- what movies were directed by [federico fellini](director)?
- what movies were directed by [john gielgud](director)?
- what are the movies by [stanley kubrick](director)?
- what are the movies by [quentin tarantino](director)?
- what are the movies by [gene kelly](director)?
- what is [gene kelly](director) known for?
- what did [gene kelly](director) create?

## intent:movie_match_actor
- what movies had the participation of [tom cruise](actor)?
- what movies had the participation of [fred astaire](actor)?
- what movies had the participation of [brigitte bardot](actor)?
- what movies had the participation of [richard burton](actor)?
- what movies had the participation of [humphrey bogart](actor)?
- what movies had the participation of [lauren bacall](actor)?
- what movies has [lauren bacall](actor) worked on?
- what movies has [brigitte bardot](actor) worked on?
- what movies has [richard burton](actor) worked on?

## intent:movie_match_year
- what were the movies made in [2018](year)?
- what were the movies made in [2019](year)?
- what were the movies made in[1995](year)?
- what were the movies made in [1999](year)?
- what were the movies made in [1980](year)?
- what movies have been released in [2018](year)?
- what movies have been released in [1990](year)?
- what movies have been released in [2000](year)?

## intent:movie_match_genre
- tell me [comedy](genre) movies
- tell me [action](genre) movies
- tell me [horror](genre) movies
- give me [comedy](genre) movies
- give me [action](genre) movies
- give me [horror](genre) movies

## intent:movie_match_language
- tell me movies in [french](language)
- tell me movies in [english](language)
- tell me movies in [portuguese](language)

## intent:movie_match_several_criteria
- tell me [comedy](genre) movies that had the participation of [tom cruise](actor)
- tell me [drama](genre) movies that had the participation of [fred astaire](actor)
- tell me movies in [french](language) that were produced between [2018](year_start) and [2019](year_end)
- tell me movies in [english](language) that were produced between [1999](year_start) and [2019](year_end)
- tell me movies in [spanish](language) that were produced between [1990](year_start) and [2002](year_end)

##intent: movie_match_rating
- what were the [top 5](rating) rated movies in [2018](year)?
- what were the [top 2](rating) rated movies in [2019](year)?
- what were the [top 10](rating) rated movies in [1990](year)?

## lookup:actor
- tom cruise
- fred astaire
- lauren bacall
- brigitte bardot
- john belushi
- ingmar bergman
- humphrey bogart
- marlon brando
- richard burton
- miguel oliveira

## lookup:director
- quentin tarantino
- ingmar bergman
- marlon brando
- james cagney
- federico fellini
- john gielgud
- charlton heston
- alfred hitchcock
- buster keaton
- gene kelly
- stanley kubrick
- gisele pereira

## lookup:genre
- comedy
- action
- horror
- drama

## lookup:language
- french
- portuguese
- english
- spanish


## regex:year
- \b(19|20)\d{2}\b

## regex:year_start
- \b(19|20)\d{2}\b

## regex:year_end
- \b(19|20)\d{2}\b

## synonym:movies
- films

## regex:rating
- top \b[0-9]+\b

## synonyms:directed
- leaded
- coordinated
- orchestrated

##synonyms:participation
- involvement
- part
- engagement
- contribution

##synonyms:made
- released
- filmed
- produced
- created
- formed

##intent:get_director_by_movie_title
- who was the director of [the godfather](movie_title)?
- who was the director of [miss jerry](movie_title)?
- who was the director of [soldiers of the cross](movie_title)?
- who was the director of [the story of the kelly gang](movie_title)?
- who was the director of [robbery under arms](movie_title)?
- who created [miss jerry](movie_title)?

##intent:get_actor_by_movie_title
- who were the star actors in [the godfather](movie_title)?
- who were the star actors in [miss jerry](movie_title)?
- who were the star actors in [soldiers of the cross](movie_title)?
- who were the star actors in [the story of the kelly gang](movie_title)?
- who were the star actors in [robbery under arms](movie_title)?

##intent:get_year_by_movie_title
- when was released [the godfather](movie_title)?
- when was released [miss jerry](movie_title)?
- when was released [soldiers of the cross](movie_title)?
- when was released [the story of the kelly gang](movie_title)?
- when was released [robbery under arms](movie_title)?
- what year did [miss jerry](movie_title) come out?

##intent:get_genre_by_movie_title
- what is the genre of [the godfather](movie_title)?
- what is the genre of [miss jerry](movie_title)?
- what is the genre of [soldiers of the cross](movie_title)?
- what is the genre of [the story of the kelly gang](movie_title)?
- what is the genre of [robbery under arms](movie_title)?

##intent:get_language_by_movie_title
- what is the language of [the godfather](movie_title)?
- what is the language of [miss jerry](movie_title)?
- what is the language of [soldiers of the cross](movie_title)?
- what is the language of [the story of the kelly gang](movie_title)?
- what is the language of [robbery under arms](movie_title)?

##intent:get_rating_by_movie_title
- what is the rating of [the godfather](movie_title)?
- what is the rating of [miss jerry](movie_title)?
- what is the rating of [soldiers of the cross](movie_title)?
- what is the rating of [the story of the kelly gang](movie_title)?
- what is the rating of [robbery under arms](movie_title)?

##lookup:movie_title
- the godfather
- miss jerry
- soldiers of the cross
- the story of the kelly gang
- robbery under arms
- joker
