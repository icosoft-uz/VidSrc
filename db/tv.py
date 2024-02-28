import json
import requests
import sqlite3


class EpisodeScraper:
    def __init__(self, base_urls=None, database_file_path="database.db"):
        if base_urls is None:
            base_urls = ["https://vidsrc.xyz/episodes/latest/", "https://vidsrc.in/episodes/latest/",
                         "https://vidsrc.pm/episodes/latest/", "https://vidsrc.net/episodes/latest/"]
        self.base_urls = base_urls
        self.database_file_path = database_file_path

    def scrape_episodes(self):
        for base_url in self.base_urls:
            page_num = 1
            while True:
                url = f"{base_url}page-{page_num}.json"

                try:
                    response = requests.get(url)
                    response.raise_for_status()  # Raise an exception for non-200 status codes

                    episode_data = json.loads(response.content)

                    # Check if there are more pages
                    if "pages" in episode_data and page_num >= episode_data["pages"]:
                        break

                    # Ensure episode_data["result"] is a list of dictionaries
                    if not isinstance(episode_data["result"], list):
                        print("Error: episode_data['result'] is not a list")
                        break

                    # Save unique episodes from the current page
                    self._save_unique_episodes_to_db(episode_data["result"])

                    page_num += 1
                except requests.exceptions.RequestException as e:
                    print(f"Error fetching page {page_num} from {base_url}: {e}")
                    break  # Stop scraping on any error

    def _save_unique_episodes_to_db(self, episodes):
        connection = sqlite3.connect(self.database_file_path)
        cursor = connection.cursor()

        # Create the table if it doesn't exist (assuming unique constraint on IMDb ID)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tv (
                imdb_id TEXT PRIMARY KEY,
                tmdb_id INTEGER,
                show_title TEXT,
                season INTEGER,
                episode INTEGER,
                embed_url TEXT,
                embed_url_tmdb TEXT DEFAULT NULL,
                quality TEXT
            )
        ''')

        for episode_data in episodes:
            # Handle non-dictionary elements
            if not isinstance(episode_data, dict):
                print("Error: episode_data is not a dictionary")
                continue

            try:
                imdb_id = episode_data["imdb_id"]

                # Check if IMDb ID already exists in the database
                cursor.execute("SELECT * FROM tv WHERE imdb_id=?", (imdb_id,))
                existing_row = cursor.fetchone()

                if existing_row:
                    # Check if existing episode has the same season and episode number
                    existing_season, existing_episode = existing_row[3], existing_row[4]
                    new_season = int(episode_data["season"])
                    new_episode_num = int(episode_data["episode"])

                    if existing_season == new_season and existing_episode == new_episode_num:
                        print(
                            f"Episode {imdb_id} (season {existing_season}, episode {existing_episode}) already exists. Skipping insertion.")
                        continue

                tmdb_id = episode_data["tmdb_id"] if episode_data["tmdb_id"] != "-1" else None
                show_title = episode_data["show_title"]
                season = int(episode_data["season"])  # Convert season to integer
                episode_num = int(episode_data["episode"])  # Convert episode to integer

                # Handle optional keys using get()
                embed_url = episode_data.get("embed_url")
                embed_url_tmdb = episode_data.get("embed_url_tmdb")
                quality = episode_data["quality"]

                cursor.execute(
                    "INSERT OR REPLACE INTO tv VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (imdb_id, tmdb_id, show_title, season, episode_num, embed_url, embed_url_tmdb, quality),
                )
            except sqlite3.IntegrityError as e:
                print(f"Error inserting episode {imdb_id}: {e}")  # Log duplicate errors

        connection.commit()
        connection.close()


if __name__ == "__main__":
    scraper = EpisodeScraper()
    scraper.scrape_episodes()
    print('Database scraped successfully!')


