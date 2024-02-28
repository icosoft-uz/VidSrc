import sqlite3


class DB:
    def __init__(self, filename='database.db'):
        self.conn = sqlite3.connect(database=filename)
        self.cursor = self.conn.cursor()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()


class Search(DB):
    def search(self, query, result_type):
        results = []

        if result_type == 1:
            # Search for movies
            self.cursor.execute("SELECT DISTINCT title FROM movies WHERE title LIKE ?", ('%' + query + '%',))
            movie_result = self.cursor.fetchall()
            results.extend(movie[0] for movie in movie_result)
        elif result_type == 2:
            # Search for TV shows
            self.cursor.execute("SELECT DISTINCT title FROM tv WHERE title LIKE ?", ('%' + query + '%',))
            tv_result = self.cursor.fetchall()
            results.extend(tv_show[0] for tv_show in tv_result)
        else:
            print("Invalid result type provided.")
            return results

        return results


if __name__ == "__main__":
    search = Search()
    movie_results = search.search("Loki", 1)  # Get movie results
    tv_results = search.search("Loki", 2)  # Get TV show results

    print("Movies:", movie_results)
    print("TV Shows:", tv_results)

