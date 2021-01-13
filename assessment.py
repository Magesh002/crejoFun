from datetime import datetime

movies = {}
users = {}
reviews = {}


def addMovie(movieName, releaseYear, genres):
    movies[movieName] = {"releaseYear": releaseYear, "genres": genres, "reviewCount": 0,
                         "totalRating": 0, "ratingPercentage": 0}


def addUser(name):
    users[name] = {"usertype": "viewer", "reviewCount": 0}


def addReviews(user, movieName, rating):
    if user in users and movieName in movies.keys():
        if int(movies.get(movieName["releaseYear"])) < datetime.now().year:
            print("Exception movie yet to be released")

        else:
            if (user, movieName) not in reviews.keys():
                reviews[(user, movieName)] = {"user": user, "movieName": movieName, "rating": rating}
                users[user]["reviewCount"] += 1
                if users[user]["reviewCount"] >= 3:
                    users[user]["usertype"] = "critic"
                movies[movieName]["totalRating"] += rating if users[user]["usertype"] == "viewer" else rating * 2
                movies[movieName]["reviewCount"] += 1
                movies[movieName]["ratingPercentage"] = movies[movieName]["totalRating"] / movies[movieName][
                    "reviewCount"]

            else:
                print("Exception multiple reviews not allowed")


def addTestData():
    addMovie(movieName="Don", releaseYear="2006", genres=["Action", "Comedy"])
    addMovie(movieName="Tiger", releaseYear="2008", genres=["Drama"])
    addMovie(movieName="Padmaavat", releaseYear="2006", genres=["Comedy"])
    addMovie(movieName="Lunchbox", releaseYear="2021", genres=["Drama"])
    addMovie(movieName="Guru", releaseYear="2006", genres=["Drama"])
    addMovie(movieName="Metro", releaseYear="2006", genres=["Romance"])

    addUser(name="SRK")
    addUser(name="Salman")
    addUser(name="Deepika")

    addReviews(user="SRK", movieName="Don", rating=2)
    addReviews(user="SRK", movieName="Padmavaat", rating=8)
    addReviews(user="Salman", movieName="Don", rating=5)
    addReviews(user="Deepika", movieName="Don", rating=9)
    addReviews(user="Deepika", movieName="Guru", rating=6)
    addReviews(user="SRK", movieName="Don", rating=10)
    addReviews(user="Deepika", movieName="Lunchbox", rating=5)
    addReviews(user="SRK", movieName="Tiger", rating=5)
    addReviews(user="SRK", movieName="Metro", rating=7)


def movieList(data, year=None, userType=None, genre=None):
    if not data:
        data = movies
    movieLists = {}
    if userType:
        userList = []
        for key, val in users.items():
            if val["usertype"] == userType:
                userList.append(key)
        for k, v in reviews.items():
            if userList and v[userType] in userList:
                movieLists[k] = v
    else:
        for k, v in data.items():
            if year and v["releaseYear"] == year:
                movieLists[k] = v
            elif genre and genre in v["genres"]:
                movieLists[k] = v

    return movieLists


addTestData()
year2006List = movieList(data=movies, year="2006")
movie = max(year2006List, key=lambda v: year2006List[v]['ratingPercentage'])
print(movie + "-" + str(movies[movie]["ratingPercentage"]) + " ratings (Some of all rating)")

movies = movieList(data=year2006List, userType="critics")
movie = max(movies, key=lambda val: movies[val]['rating'])
print(reviews[movie]["movieName"] + "-" + str(reviews[movie]["rating"] * 2) + " ratings (only " + movies[movie][
    "user"] + " gave " + movies[movie]["rating"] + " for Metro as critic)")

genreList = movieList(data=movies, genre="Drama")
movie = max(genreList, key=lambda v: genreList[v]['ratingPercentage'])
print(movie + "-" + str(movies[movie]["ratingPercentage"]) + " ratings")

count = 0
rate = 0
s = "("
for x, y in year2006List.items():
    for q, w in reviews.items():
        if y["movieName"] == w["movieName"]:
            count += 1
            rate += w["rating"]
            s += str(w["rating"])
s += ")/" + str(count) + " = " + str(rate / count) + "ratings (7 of \"Metro\" considered twice since it was submitted by critic)"
