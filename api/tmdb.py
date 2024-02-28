import requests
import json


def search(query, page):
    url = f"https://api.themoviedb.org/3/search/movie?query={query}&page={page}"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0M2RjZDliNGVmZTMwOTM5MjMyYTM5Y2ZmYjU0OWQ4YiIsInN1YiI6IjY1ZDY0YjdiYzVjMWVmMDE0YThhZTU5MCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.qo1zPAvFmAk6_0gLwTLnKj7ZBfpIGyoFaJWfycMQfQQ"
    }
    response = requests.get(url, headers=headers)
    return json.dumps(response.json(), indent=4, sort_keys=True)


if __name__ == "__main__":
    data = search('oppenheimer', 1)
    print(data)
