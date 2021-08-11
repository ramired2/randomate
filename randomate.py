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
    country = 'US'
    
    # when entering diff country
    # json file that has countries n abbrevs needed
    p = request.form.get('p')
    n = request.form.get('n')
    if p and n:
        n=int(n)
        country = p
        dataCharts = read(p.strip(), n)
    elif p:
        country = p
        dataCharts = read(p.strip(), 10)
    else:
        dataCharts = read('us', 10)

    # when entering playlist search
    q = request.args.get("q")
    size = request.args.get("size")
    # print(size)
    if q and size:
        size=int(size)
        print(size)
        processSearch(q, size)
        
        with open("dataSearch.json", 'r') as j:
            dataPlaylists = json.loads(j.read())
        return render_template("search.html", title="Search "+q, search=q, dataPlaylists=dataPlaylists)
    elif q:
        print("just q")
        processSearch(q, 5)
        
        with open("dataSearch.json", 'r') as j:
            dataPlaylists = json.loads(j.read())
        return render_template("search.html", title="Search "+q, search=q, dataPlaylists=dataPlaylists)

    return render_template("homepage.html", title="Home", dataCharts=dataCharts, countries=countries, selected=country.upper())

# specific page for getting playlists, must input number if using this link
@app.route("/search/<query>/<num>", methods=["GET", "POST"])
def search(query, num):

    q = request.args.get("q")
    size = request.args.get("size")

    if q and size:
        size=int(size)
        processSearch(q, size)
        
        with open("dataSearch.json", 'r') as j:
            dataPlaylists = json.loads(j.read())
        return render_template("search.html", title="Search "+q, search=q, dataPlaylists=dataPlaylists)
    elif q:
        processSearch(q, 5)
        
        with open("dataSearch.json", 'r') as j:
            dataPlaylists = json.loads(j.read())
        return render_template("search.html", title="Search "+q, search=q, dataPlaylists=dataPlaylists)
    elif query and num:
        num=int(num)
        processSearch(query, num)
        with open("dataSearch.json", 'r') as j:
                dataPlaylists = json.loads(j.read())
        return render_template("search.html", title="Search "+query.upper(), search=query, dataPlaylists=dataPlaylists)
    elif query:
        processSearch(query, 5)
        with open("dataSearch.json", 'r') as j:
                dataPlaylists = json.loads(j.read())
        return render_template("search.html", title="Search "+query.upper(), search=query, dataPlaylists=dataPlaylists)


# FOR ERRORS

@app.errorhandler(404)
def not_found(error):
    q = request.args.get("q")
    size = request.args.get("size")

    if q and size:
        size=int(size)
        print(size)
        processSearch(q, size)
        
        with open("dataSearch.json", 'r') as j:
            dataPlaylists = json.loads(j.read())
        return render_template("search.html", title="Search "+q, search=q, dataPlaylists=dataPlaylists)
    elif q:
        # print("just q")
        processSearch(q, 5)
        
        with open("dataSearch.json", 'r') as j:
            dataPlaylists = json.loads(j.read())
        return render_template("search.html", title="Search "+q, search=q, dataPlaylists=dataPlaylists)
    return render_template("error.html")

if __name__ == '__main__':
    app.run(debug=True)