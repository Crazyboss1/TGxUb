from imdb import Cinemagoer

imdb = Cinemagoer()

async def get_poster(query, bulk=False, id=False):
    try:
        if not id:
            # Searching for movies
            search_results = imdb.search_movie(query)
            if not search_results:
                return None
            
            if bulk:
                # Return multiple results for bulk search
                return [
                    {
                        'title': movie.get('title', 'N/A'),
                        'year': movie.get('year', 'N/A'),
                        'imdb_id': movie.movieID
                    }
                    for movie in search_results[:5]  # Limit to top 5 results
                ]
            
            # Single result for non-bulk search
            movie = search_results[0]
            movie_id = movie.movieID
        else:
            # Direct lookup by IMDb ID
            movie_id = query

        # Fetch detailed movie information
        movie = imdb.get_movie(movie_id)
        if not movie:
            return None

        # Extract relevant information
        title = movie.get('title', 'N/A')
        year = movie.get('year', 'N/A')
        genres = ', '.join(movie.get('genres', [])) if movie.get('genres') else 'N/A'
        languages = ', '.join(movie.get('languages', [])) if movie.get('languages') else 'Original Audio'
        rating = movie.get('rating', 'N/A')
        plot = movie.get('plot outline', 'N/A') if movie.get('plot outline') else (movie.get('plot', ['N/A'])[0] if movie.get('plot') else 'N/A')
        poster = movie.get('full-size cover url', 'N/A')
        url = f'https://www.imdb.com/title/tt{movie_id}'

        return {
            'title': title,
            'year': year,
            'genres': genres,
            'languages': languages,
            'rating': rating,
            'plot': plot,
            'poster': poster,
            'imdb_id': movie_id,
            'url': url
        }

    except Exception as e:
        print(f"Error in get_poster: {str(e)}")
        return None
