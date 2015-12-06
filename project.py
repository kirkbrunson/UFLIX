import urlparse
from flask import Flask, render_template, request
from tmdb3 import set_key, searchMovie, Movie

app = Flask(__name__)

# Set api key for TMDb
set_key('TMDB_API_KEY')


# Route for home page 
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')


# Route for search & results
@app.route('/search/', methods=['GET', 'POST'])
def search():
    # Get user's query from the url
    query = request.query_string[2:]

    if query != '':
        # Pass query to api and render results in template. If no res then show error template
        while True:
            try:
                results = searchMovie(query)
                print results[0]            # this way to test is annoying... should be more elegant
                return render_template('search_results.html', results=results)
                break

            except:
                return render_template('search_error.html')

    # Handle w. search w. blank query
    elif query == '':
        return render_template('search_blank.html')
    
    else:
        return render_template('search_error.html')
    

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)