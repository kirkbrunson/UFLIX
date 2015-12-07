import urlparse
from flask import Flask, render_template, request
from tmdb3 import set_key, searchMovie, Movie

app = Flask(__name__)

# Set api key for TMDb
set_key('TMDB_API_KEY')

# Home page 
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')


# Search & results
@app.route('/search/', methods=['GET', 'POST'])
def search():
    # Get query from url
    query = request.query_string[2:]

    if query != '':
        try:
            # TODO: Catch IO_err
            res = searchMovie(query)
            movies = []
            
            # Filter results
            for i in res:
                try:
                    i.img = i.poster.geturl('w342')

                    # If YT Trailer, keep the movie
                    if i.youtube_trailers[0] != None:
                        i.trailer = i.youtube_trailers[0].geturl()
                        movies.append(i)

                        # TODO: Format cast & gernre strings
                except:
                    pass

            return render_template('search_results.html', results=movies)
        
        # Catch all other errors
        except:
            return render_template('search_error.html')

    # Handle blank query
    elif query == '':
        return render_template('search_blank.html')

    else:
        return render_template('search_error.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
