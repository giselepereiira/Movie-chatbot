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
- what movies were directed by [charlton heston](director)?
- what movies were directed by [alfred hitchcock](director)?
- what movies were directed by [buster keaton](director)?
- what movies were directed by [stanley kubrick](director)?

## intent:movie_match_actor
- what movies had the participation of [tom cruise](actor)?
- what movies had the participation of [fred astaire](actor)?
- what movies had the participation of [brigitte bardot](actor)?
- what movies had the participation of [richard burton](actor)?
- what movies had the participation of [humphrey bogart](actor)?
- what movies had the participation of [lauren bacall](actor)?

## intent:movie_match_top_rated_year
- what were the top rated movies in [2018](year)?
- what were the top rated movies in [2019](year)?
- what were the top rated movies in [1995](year)?
- what were the top rated movies in [1999](year)?
- what were the top rated movies in [1980](year)?

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
