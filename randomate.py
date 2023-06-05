from flask import Flask, render_template, url_for, request
app = Flask(__name__)

import json
from search import processSearch, getTracks
from top import read, billboardCategories, billboardTracks, categoryLinkToTitle

@app.route("/")
@app.route("/homepage", methods=['GET', 'POST'])
def homepage():

    #get the categories -- just in case changes at some point
    billboardCategories()

    # spotify removed this function
    with open("categories.json", 'r') as l:
            category = json.loads(l.read())

    # playlist = request.args.get("playlist")
    # print(playlist)
    # if playlist:
        # print(playlist)
        # playlist = playlist.split()
        # plylist id --> print(playlist[0])
        # creator id --> print(playlist[1])
        # getTracks()
    
    # when entering diff category to look at
    p = request.args.get('p')
    n = request.args.get('n')

    print(p) # category
    print(n) #number

    # when choosing a diff category/ num items
    if p and n:
        n=int(n)
        chosenCategory = p
        print("p and num: ", p, n, "\n")
        dataCharts = billboardTracks(p.strip(), n)
        chosenCategory = categoryLinkToTitle(p)
    elif p:
        chosenCategory = p
        print("p only: ", p, "\n")
        dataCharts = billboardTracks(p.strip(), 100)
        chosenCategory = categoryLinkToTitle(p)
    else:
        dataCharts = billboardTracks("/charts/hot-100/", 10)
        chosenCategory="Hot 100"

    # when entering playlist search
    q = request.args.get("q")
    size = request.args.get("size")


    # to track current p and size for if you choose a playlist tracks
    chose = ""
    if q:
        jsonInfo = []
        jsonInfo.append({'p':q, 'size':size})
        jsonString = json.dumps(jsonInfo, indent=4)
        jsonFile = open("dataLastSearch.json", "w")
        jsonFile.write(jsonString)
        jsonFile.close()


    if q and size:
        size=int(size)
        print(size)
        processSearch(q, size)
        
        with open("dataSearch.json", 'r') as j:
            dataPlaylists = json.loads(j.read())   
        return render_template("search.html", title="Search "+q, search=q.capitalize(), dataPlaylists=dataPlaylists, chose=chose.capitalize())
    elif q:
        print("just q")
        processSearch(q, 5)
        
        with open("dataSearch.json", 'r') as j:
            dataPlaylists = json.loads(j.read())
        return render_template("search.html", title="Search "+q, search=q.capitalize(), dataPlaylists=dataPlaylists, chose=chose.capitalize())

    playlist = request.args.get("playlist")
    print("playlist is: ")
    print(playlist)
    if playlist:
        playlist = playlist.split()
        print(len(playlist))
        # print(playlist[0])
        # print(playlist[1])
        # print(playlist[2])


        with open("dataLastSearch.json", 'r') as x:
            lastSearch = json.loads(x.read())
            for jsonObj in x:
                searchDict = json.loads(jsonObj)
                lastSearch.append(searchDict)
            
            for serch in lastSearch:
                q = json.dumps(serch["p"])
                q = q.replace('"','')
                size = json.dumps(serch["size"])
                size = size.replace('"','')
                print(q)
                print(size)

        # call function to do search for getTracks
        chose = getTracks(playlist[0])


        with open("dataTracks.json", 'r') as s:
            songs = json.loads(s.read())
        
        # if only q then this
        if q and size:
            # size = size.strip()
            size = int(size)
            processSearch(q, size)
            with open("dataSearch.json", 'r') as j:
                dataPlaylists = json.loads(j.read())

            return render_template("search.html", title="Search "+q, search=q.capitalize(), dataPlaylists=dataPlaylists, songs=songs, chose=chose, choseid=playlist[0])

        # else if q and size
        else:
            processSearch(q, 5)
            with open("dataSearch.json", 'r') as j:
                dataPlaylists = json.loads(j.read())

            return render_template("search.html", title="Search "+q, search=q.upper(), dataPlaylists=dataPlaylists, songs=songs, chose=chose.capitalize(), choseid=playlist[0])

    # return render_template("homepage.html", title="Home", dataCharts=dataCharts, countries=countries, selected=country.upper())
    return render_template("homepage.html", title="Home", dataCharts=dataCharts, category=category, selected=chosenCategory)

# specific page for getting playlists, must add number if using this link
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


# link to just receive the info for playlists
@app.route("/info/playlist/<word>/<size>", methods=["GET", "POST"])
def info(word, size):
    processSearch(word, size)
    with open("dataSearch.json", 'r') as j:
            infos = json.loads(j.read())
    return render_template("info.html", infos=json.dumps(infos, indent=4))
    # return json.dumps(infos, indent=4)

# link to just receive the info for x country top tracks
# @app.route("/info/top/<country>/<num>", methods=["GET", "POST"])
# def infoCountry(country, num):
#     num = int(num)
#     infos = read(country, num)
#     # with open("dataTop.json", 'r') as j:
#     #         infos = json.loads(j.read())
#     return render_template("info.html", infos=json.dumps(infos, indent=4))
#     # return json.dumps(infos, indent=4)



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
    # app.run(host="0.0.0.0", port=8430)
    app.run(debug=True)