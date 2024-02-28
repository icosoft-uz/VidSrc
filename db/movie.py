import json
import requests
import sqlite3


class MovieScraper:
    def __init__(self, base_urls=None, database_file_path='database.db'):
        if base_urls is None:
            base_urls = ['https://vidsrc.xyz/movies/latest/', 'https://vidsrc.in/movies/latest/',
                         'https://vidsrc.pm/movies/latest/', 'https://vidsrc.net/movies/latest/']
        self.base_urls = base_urls
        self.database_file_path = database_file_path

    def scrape_movies(self):
        for base_url in self.base_urls:
            page_num = 1
            while True:
                url = f"{base_url}page-{page_num}.json"

                try:
                    response = requests.get(url)
                    response.raise_for_status()  # Raise an exception for non-200 status codes

                    movie_data = json.loads(response.content)

                    # Check if there are more pages
                    if "pages" in movie_data and page_num >= movie_data["pages"]:
                        break

                    self._save_unique_movies_to_db(movie_data["result"])

                    page_num += 1
                except requests.exceptions.RequestException as e:
                    print(f"Error fetching page {page_num} from {base_url}: {e}")
                    break  # Stop scraping on any error

    def _save_unique_movies_to_db(self, movies):
        connection = sqlite3.connect(self.database_file_path)
        cursor = connection.cursor()

        # Create a table if it doesn't exist (assuming unique constraint on imdb_id)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS movies (
                imdb_id TEXT PRIMARY KEY,
                tmdb_id INTEGER,
                title TEXT,
                embed_url TEXT,
                embed_url_tmdb TEXT DEFAULT NULL,
                quality TEXT
            )
        ''')

        for movie in movies:
            imdb_id = movie["imdb_id"]
            cursor.execute("SELECT 1 FROM movies WHERE imdb_id=?", (imdb_id,))
            if not cursor.fetchone():  # Movie not found in the table
                try:
                    tmdb_id = movie["tmdb_id"] if movie["tmdb_id"] != "-1" else None
                    title = movie["title"]
                    embed_url = movie["embed_url"]
                    embed_url_tmdb = movie.get("embed_url_tmdb")  # Use get() with default value
                    quality = movie["quality"]

                    cursor.execute(
                        "INSERT INTO movies VALUES (?, ?, ?, ?, ?, ?)",
                        (imdb_id, tmdb_id, title, embed_url, embed_url_tmdb, quality),
                    )
                except sqlite3.IntegrityError as e:
                    print(f"Error inserting movie {imdb_id}: {e}")  # Log duplicate errors

        connection.commit()
        connection.close()


if __name__ == "__main__":
    scraper = MovieScraper()
    scraper.scrape_movies()

    print("Database scraped successfully!")
