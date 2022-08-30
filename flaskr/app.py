from flask import Flask, render_template, render_template_string, json, request, make_response
import sys
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text 

app = Flask(__name__)

CLOUD_SQL_DB = "CrimeSearchDatabase"
CLOUD_SQL_USERNAME = "root"
CLOUD_SQL_PASSWORD = "AryaStephNeha#123"
CLOUD_SQL_IP = "34.121.148.188"
CLOUD_SQL_CONNECTION = "intense-howl-342117:us-central1:neha-instance"

app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+mysqldb://{CLOUD_SQL_USERNAME}:{CLOUD_SQL_PASSWORD}@{CLOUD_SQL_IP}/{CLOUD_SQL_DB}?unix_socket=/cloudsql/{CLOUD_SQL_CONNECTION}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)

@app.route("/")
def home():
    return render_template("index.html", name="Stops & Searches and Crimes")

@app.route("/person", methods=["GET"])
def person_get():
    results = db.engine.execute("SELECT * FROM Person LIMIT 15;")

    return render_template("person.html", query_result=results)

@app.route("/person", methods=["DELETE"])
def person_delete():
    #delete
    return render_template("person.html", query_result=[])

@app.route("/crime", methods=["GET"])
def crime_search():
    crime_type = request.args.get("type")
    if crime_type is not None:
        results = db.engine.execute(text("SELECT * FROM Crime WHERE CategoryCrime LIKE :query;"), query=f"%{crime_type}%")
    else:
        results = db.engine.execute("SELECT * FROM Crime;")
    return render_template("crime-search.html", query_result=results)

@app.route("/location", methods=["GET"])
def location_search():
    location_type = request.args.get("type")
    if location_type is not None:
        results = db.engine.execute(text("SELECT * FROM Location WHERE StreetName LIKE :query;"), query=f"%{location_type}%")
    else:
        results = db.engine.execute("SELECT * FROM Location;")
    return render_template("location-search.html", query_result=results)


@app.route("/loglocation", methods=["GET", "POST"])
def log_location():
    if request.method == 'GET':
        return render_template("location-log.html")
    
    crimeid = request.json.get("CrimeID")
    latitude = request.json.get("Latitude")
    longitude = request.json.get("Longitude")
    crimelevel = request.json.get("CrimeLevel")
    streetname = request.json.get("StreetName")
    db.engine.execute(f'INSERT INTO Location(CrimeID, Latitude, Longitude, CrimeLevel, StreetName) VALUES ("{crimeid}", "{latitude}", "{longitude}", "{crimelevel}", "{streetname}");')

    return make_response({"message": f"successfully logged location with id={crimeid}"}, 201)


@app.route("/logcrime", methods=["GET", "POST"])
def log_crime():
    if request.method == 'GET':
        return render_template("crime-log.html")
    
    crimeid = request.json.get("CrimeID")
    category = request.json.get("CategoryCrime")
    outcome = request.json.get("LastOutcome")
    db.engine.execute(f'INSERT INTO Crime(CrimeID, CategoryCrime, LastOutcome) VALUES ("{crimeid}", "{category}", "{outcome}");')

    return make_response({"message": f"successfully logged crime with id={crimeid}"}, 201)

@app.route("/updatecrime", methods=["GET", "POST"])
def update_crime():
    if request.method == 'GET':
        return render_template("updatecrime.html")
    else:
        crimeid = request.json.get("CrimeID")
        category = request.json.get("CategoryCrime")
        outcome = request.json.get("LastOutcome")
        db.engine.execute(f'UPDATE Crime SET CrimeID="{crimeid}" , CategoryCrime="{category}" , LastOutcome="{outcome}" WHERE CrimeID = "{crimeid}" ;')

        return make_response({"message": f"successfully updated crime with id={crimeid}"}, 201)

@app.route("/deletecrime", methods=["GET", "POST"])
def delete_crime():
    if request.method == 'GET':
        return render_template("deletecrime.html")
    else:
        crimeid = request.json.get("CrimeID")
        category = request.json.get("CategoryCrime")
        outcome = request.json.get("LastOutcome")
        db.engine.execute(f'DELETE FROM Crime WHERE CrimeID="{crimeid}";')
        return make_response({"message": f"successfully deleted crime with id={crimeid}"}, 201)


    #return render_template("updatecrime.html")
    # if (request.method == "POST"):
    #     personid = request.json.get("PersonID")
    #     agerange=request.json.get("AgeRange")
    #     selfeth = request.json.get("SelfDescribedEthnicity")
    #     officereth = request.json.get("OfficerDescribedEthnicity")
    #     gender = request.json.get("Gender")
    #     db.engine.execute("UPDATE Person SET AgeRange=\'{}\' , SelfDescribedEthnicity=\'{}\' ,  OfficerDescribedEthnicity=\'{}\' , Gender=\'{}\' WHERE PersonID = {};").format(agerange, selfeth, officereth, gender, personid)
    # else:
    

@app.route("/analysis", methods=["GET"])
def analysis_show1():
    #post
    results = db.engine.execute(text("(SELECT COUNT(PersonID) AS countpersons, s.Outcome FROM Person p NATURAL JOIN Search s WHERE (p.SelfDescribedEthnicity like '%Black%' OR p.SelfDescribedEthnicity like '%African%') AND (s.ObjectOfSearch LIKE '%Drug%') GROUP BY s.Outcome) UNION (SELECT COUNT(PersonID) AS countpersons, s.Outcome FROM Person p NATURAL JOIN Search s WHERE (p.SelfDescribedEthnicity like '%White%' OR p.SelfDescribedEthnicity like '%British%') AND (s.ObjectOfSearch LIKE '%Drug%') GROUP BY s.Outcome)"))
    return render_template("analysis.html", query_result=results)

@app.route("/analysis2", methods=["GET"])
def analysis_show2():
    #post
    results = db.engine.execute(text("SELECT COUNT(CrimeID) AS countcrimes, l.StreetName FROM Crime c NATURAL JOIN Location l WHERE (c.CategoryCrime LIKE '%Anti_social behaviour%') OR (c.CategoryCrime LIKE '%Public order%') OR (c.CategoryCrime LIKE '%Shoplifting%') OR (c.CategoryCrime LIKE '%Bicycle theft%') GROUP BY l.StreetName"))
    return render_template("analysis2.html", query_result=results)

@app.route("/storedproc", methods=["POST"])
def storedproc_show():
    #post
    conn = db.engine.raw_connection()
    try:
        cursor = conn.cursor()
        cursor.callproc("legislationDisparities", [])
        results = list(cursor.fetchall())
        cursor.close()
        conn.commit()
        return render_template("index.html")
    finally:
        conn.close()
    #return render_template("storedproc.html", query_result=results)


@app.route("/insert", methods=["GET"])
def insert_get():
    return render_template("insert.html")

@app.route("/delete", methods=["GET"])
def delete_get():
    return render_template("delete.html")


