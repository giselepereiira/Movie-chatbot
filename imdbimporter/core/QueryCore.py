from imdbimporter.database.DatabaseConstants import session

from imdbimporter.models.Title import Title

def get_movie_title_by_year(year):
    x = session.query(Title.title).filter(Title.year == year).all()

    print(x)

if __name__ == '__main__':
    get_movie_title_by_year(1890)