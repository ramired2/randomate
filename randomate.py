from flask import Flask, render_template, url_for, request
app = Flask(__name__)

import json
from search import processSearch
from top import read

@app.route("/")
@app.route("/homepage", methods=['GET', 'POST'])
def homepage():

    with open("countriesSpotify.json", 'r') as l:
            countries = json.loads(l.read())
    
    # when entering diff country
    # json file that has countries n abbrevs needed
    p = request.form.get('p')
    if p:
        dataCharts = read(p.strip(), 10)
    else:
        dataCharts = read('us', 10)

    # when entering playlist search
    q = request.args.get("q")
    if q:
        processSearch(q, 5)
        
        with open("dataSearch.json", 'r') as j:
            dataPlaylists = json.loads(j.read())
        return render_template("search.html", title="Search "+q, search=q, dataPlaylists=dataPlaylists)

    return render_template("homepage.html", title="Home", dataCharts=dataCharts, countries=countries)

# specific page for getting playlists
@app.route("/search/<query>", methods=["GET", "POST"])
def search(query):

    q = request.args.get("q")
    if q:
        processSearch(q, 5)
        with open("dataSearch.json", 'r') as j:
            dataPlaylists = json.loads(j.read())
        return render_template("search.html", title="Search "+q, search=q, dataPlaylists=dataPlaylists)

    processSearch(query, 5)
    with open("dataSearch.json", 'r') as j:
            dataPlaylists = json.loads(j.read())
    return render_template("search.html", title="Search "+query, search=query, dataPlaylists=dataPlaylists)

# FOR ERRORS

@app.errorhandler(404)
def not_found(error):
    q = request.args.get("q")
    if q:
        processSearch(q, 5)
        # dataPlaylists = json.load(g)
        with open("dataSearch.json", 'r') as j:
            dataPlaylists = json.loads(j.read())
        return render_template("search.html", title="Search "+q, search=q, dataPlaylists=dataPlaylists)
    return render_template("error.html")

if __name__ == '__main__':
    app.run(debug=True)