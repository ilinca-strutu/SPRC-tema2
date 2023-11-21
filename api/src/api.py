from http import HTTPStatus
import json
from flask import request, jsonify, Flask, Response
import os
import psycopg2

app = Flask(__name__)

# 200 - OKAY
# 400 - BAD REQ
# 404 - NOT FOUND
# 409 - CONFLICT -> inseram de 2 ori acelasi 

@app.route("/api/countries", methods = ["GET"])
def api_countries_get():
    my_db = psycopg2.connect(
        database=str(os.environ['DB_NAME']),
        user=str(os.environ['DB_USER']),
        password=str(os.environ['DB_PASSWORD']),
        host=str(os.environ['DB_HOST']))
    cursor = my_db.cursor()
    
    cursor.execute("select * from tari")
    get_tari = cursor.fetchall()
    
    cursor.close()
    my_db.close()
    
    return jsonify([{"id" : get_tari[i][0], "nume" : get_tari[i][1],
                    "lat" : get_tari[i][2], "lon" : get_tari[i][3]} 
                    for i in range(len(get_tari))]), 200


@app.route("/api/countries", methods = ["POST"])
def api_countries_post() :
    req = request.get_json(silent = True)
    if(not req or "nume" not in req or "lat" not in req or "lon" not in req) :
        return Response(status=400)
    else :        
        my_db = psycopg2.connect(
            database=str(os.environ['DB_NAME']),
            user=str(os.environ['DB_USER']),
            password=str(os.environ['DB_PASSWORD']),
            host=str(os.environ['DB_HOST']))
        cursor = my_db.cursor()

        try :
            cursor.execute("insert into tari (nume_tara, latitudine, longitudine) values (%s, %s, %s)",
                    (str(req["nume"]), str(req["lat"]), str(req["lon"])))
        except psycopg2.IntegrityError:
            return Response(status=409) 

        my_db.commit()

        cursor.execute("select id from tari where nume_tara = \'" + req["nume"] + "\'")
        post_id = cursor.fetchone()

        cursor.close()
        my_db.close()

        return jsonify({"id" : post_id[0]}), 201


@app.route("/api/countries/<int:id>", methods = ["PUT"])
def api_countries_put(id) :
    req = request.get_json(silent = True)
    if(not req or "id" not in req or "nume" not in req or "lat" not in req or "lon" not in req or id != req["id"] ) :
        return Response(status=400)
    else :
        my_db = psycopg2.connect(
            database=str(os.environ['DB_NAME']),
            user=str(os.environ['DB_USER']),
            password=str(os.environ['DB_PASSWORD']),
            host=str(os.environ['DB_HOST']))
        cursor = my_db.cursor()

        cursor.execute("select * from tari where id = %s", (str(id),))
        select_id = cursor.fetchall()
        if len(select_id) == 0 :
            return Response(status=404)
        try :
            cursor.execute("update tari set nume_tara = %s, latitudine = %s, longitudine = %s where id = %s",
                        (str(req["nume"]), str(req["lat"]), str(req["lon"]), str(id)))
        except psycopg2.IntegrityError :
            return Response(status=409)
        my_db.commit()

        cursor.close()
        my_db.close()

        return Response(status=200)

@app.route("/api/countries/<int:id>", methods = ["DELETE"])
def api_countries_delete(id):
    my_db = psycopg2.connect(
        database=str(os.environ['DB_NAME']),
        user=str(os.environ['DB_USER']),
        password=str(os.environ['DB_PASSWORD']),
        host=str(os.environ['DB_HOST']))
    cursor = my_db.cursor()

    cursor.execute("select * from tari where id = %s", (str(id),))
    select_del = cursor.fetchall()
    if len(select_del) == 0 :
        return Response(status=404)

    cursor.execute("delete from tari where id = %s", (str(id), ))

    my_db.commit()

    cursor.close()
    my_db.close()

    return Response(status=200)

@app.route("/api/cities", methods = ["POST"])
def api_cities_post():
    req = request.get_json(silent = True)
    if(not req or "idTara" not in req or "nume" not in req or "lat" not in req or "lon" not in req) :
        return Response(status=400)
    else :
        my_db = psycopg2.connect(
            database=str(os.environ['DB_NAME']),
            user=str(os.environ['DB_USER']),
            password=str(os.environ['DB_PASSWORD']),
            host=str(os.environ['DB_HOST']))
        cursor = my_db.cursor()

        try :
            cursor.execute("insert into orase (id_tara, nume_oras, latitudine, longitudine) values (%s, %s, %s, %s)",
                    (str(req["idTara"]), str(req["nume"]), str(req["lat"]), str(req["lon"]))
                    )
        except psycopg2.IntegrityError:
            return Response(status=409) 

        my_db.commit()

        cursor.execute("select id from orase where nume_oras = \'" + req["nume"] + "\'")
        select_orase = cursor.fetchone()

        cursor.close()
        my_db.close()

        return jsonify({"id" : select_orase[0]}), 201
   
@app.route("/api/cities", methods = ["GET"])
def api_cities_get():
    my_db = psycopg2.connect(
        database=str(os.environ['DB_NAME']),
        user=str(os.environ['DB_USER']),
        password=str(os.environ['DB_PASSWORD']),
        host=str(os.environ['DB_HOST']))
    cursor = my_db.cursor()

    cursor.execute("select * from orase")
    select_orase = cursor.fetchall()

    cursor.close()
    my_db.close()
    
    return jsonify([{"id" : select_orase[i][0], "idTara" : select_orase[i][1],
                    "nume" : select_orase[i][2], "lat" : select_orase[i][3],
                    "lon" : select_orase[i][4]} 
                    for i in range(len(select_orase))]), 200

@app.route("/api/cities/country/<int:id_Tara>", methods = ["GET"])
def api_cities_country_get(id_Tara) :
    my_db = psycopg2.connect(
        database=str(os.environ['DB_NAME']),
        user=str(os.environ['DB_USER']),
        password=str(os.environ['DB_PASSWORD']),
        host=str(os.environ['DB_HOST']))
    cursor = my_db.cursor()

    cursor.execute("select * from orase where id_tara = %s", (str(id_Tara),))
    select_orase = cursor.fetchall()

    cursor.close()
    my_db.close()
    
    if(len(select_orase) == 0) :
        return jsonify([]), 200

    return jsonify([{"id" : select_orase[i][0], "idTara" : select_orase[i][1],
                    "nume" : select_orase[i][2], "lat" : select_orase[i][3],
                    "lon" : select_orase[i][4]} 
                    for i in range(len(select_orase))]), 200

@app.route("/api/cities/<int:id>", methods = ["PUT"])
def api_cities_put(id) :
    req = request.get_json(silent = True)
    if(not req or "id" not in req or "idTara" not in req or "nume" not in req or "lat" not in req or "lon" not in req or id != req["id"]) :
        return Response(status=400)
    else :
        my_db = psycopg2.connect(
            database=str(os.environ['DB_NAME']),
            user=str(os.environ['DB_USER']),
            password=str(os.environ['DB_PASSWORD']),
            host=str(os.environ['DB_HOST']))
        cursor = my_db.cursor()

        cursor.execute("select * from orase where id = %s", (str(id)))
        select_orase = cursor.fetchall()
        if len(select_orase) == 0 :
            return Response(status=404)
        try :
            cursor.execute("update orase set id_tara = %s, nume_oras = %s, latitudine = %s, longitudine = %s where id = %s",
                        (str(req["idTara"]), str(req["nume"]), str(req["lat"]), str(req["lon"]), str(id)))
        except psycopg2.IntegrityError :
            return Response(status=409)
        my_db.commit()

        cursor.close()
        my_db.close()

        return Response(status=200)
  

@app.route("/api/cities/<int:id>", methods = ["DELETE"])
def api_cities_delete(id):
    my_db = psycopg2.connect(
        database=str(os.environ['DB_NAME']),
        user=str(os.environ['DB_USER']),
        password=str(os.environ['DB_PASSWORD']),
        host=str(os.environ['DB_HOST'])
    )
    cursor = my_db.cursor()

    cursor.execute("select * from orase where id = %s", (str(id),))
    select_orase = cursor.fetchall()
    if len(select_orase) == 0 :
        return Response(status=404)

    cursor.execute("delete from orase where id = %s", (str(id), ))

    my_db.commit()

    cursor.close()
    my_db.close()

    return Response(status=200)

@app.route("/api/temperatures", methods = ["POST"])
def api_temps_get() :
    req = request.get_json(silent = True)
    if(not req or "id_oras" not in req or "valoare" not in req):
        return Response(status=400)
    else :
        my_db = psycopg2.my_dbect(
            database=str(os.environ['DB_NAME']),
            user=str(os.environ['DB_USER']),
            password=str(os.environ['DB_PASSWORD']),
            host=str(os.environ['DB_HOST']))
        cursor = my_db.cursor()

        try :
            cursor.execute("insert into temperaturi (valoare, id_oras) values (%s, %s) returning id",
                    (str(req["valoare"]), str(req["id_oras"])))
        except psycopg2.IntegrityError:
            return Response(status=409)
        post_id = cursor.fetchone()

        my_db.commit()

        cursor.close()
        my_db.close()

        return jsonify({"id" : post_id[0]}), 201

select_string = "select id, valoare, to_date(to_char(timestamp, 'YYYY-MM-DD'), 'YYYY-MM-DD') as timestamp from temperaturi "
select_oras_string = "select id, valoare, to_date(to_char(timestamp, 'YYYY-MM-DD'), 'YYYY-MM-DD') as timestamp from temperaturi where id_oras = {t} "
lat_string = "id_oras in (select id from orase where latitudine = {t}) "
lon_string = "id_oras in (select id from orase where longitudine = {t}) "
from_string = "to_date(to_char(timestamp, 'YYYY-MM-DD'), 'YYYY-MM-DD') >= to_date('{t}','YYYY-MM-DD') "
until_string = "to_date(to_char(timestamp, 'YYYY-MM-DD'), 'YYYY-MM-DD') <= to_date('{t}','YYYY-MM-DD') "

@app.route("/api/temperatures", methods = ["GET"])
def api_temps() :
        
    get_string = select_string

    args = request.args.to_dict()

    if len(args) > 0 :
        no_arg = len(args)
        get_string += "where "

        if "lat" in args :
            get_string += lat_string.format(t = str(args["lat"]))
            if no_arg > 1 :
                no_arg -= 1
                get_string += "and "
            
        if "lon" in args :
            get_string += lon_string.format(t = str(args["lon"]))
            if no_arg > 1 :
                no_arg -= 1
                get_string += "and "

        if "from" in args :
            get_string += from_string.format(t = str(args["from"]))
            if no_arg > 1 :
                no_arg -= 1
                get_string += "and "

        if "until" in args :
            get_string += until_string.format(t = str(args["until"]))
            if no_arg > 1 :
                no_arg -= 1
                get_string += "and "

    my_db = psycopg2.connect(
        database=str(os.environ['DB_NAME']),
        user=str(os.environ['DB_USER']),
        password=str(os.environ['DB_PASSWORD']),
        host=str(os.environ['DB_HOST']))
    cursor = my_db.cursor()

    cursor.execute(get_string)
    get_temps = cursor.fetchall()

    cursor.close()
    my_db.close()
    
    if(len(get_temps) == 0) :
        return jsonify([]), 200
    
    return jsonify([{"id" : get_temps[i][0], "valoare" : get_temps[i][1],
                    "timestamp" : get_temps[i][2]}
                    for i in range(len(get_temps))]), 200

@app.route("/api/temperatures/<int:id>", methods = ["PUT"])
def api_temps_put(id):
    req = request.get_json(silent = True)
    if(not req or id != req["id"] or "id" not in req or "idOras" not in req or "valoare" not in req ) :
        return Response(status=400)
    else :
        my_db = psycopg2.connect(
            database=str(os.environ['DB_NAME']),
            user=str(os.environ['DB_USER']),
            password=str(os.environ['DB_PASSWORD']),
            host=str(os.environ['DB_HOST']))
        cursor = my_db.cursor()

        cursor.execute("select * from temperaturi where id = %s", (str(id),))
        select_temps = cursor.fetchall()
        if len(select_temps) == 0 :
            return Response(status=404)
        
        try :
            cursor.execute("update temperaturi set valoare = %s, timestamp = NOW(), id_oras = %s, where id = %s",
                        (str(req["valoare"]), str(req["idOras"]), str(id)))
        except psycopg2.IntegrityError :
            return Response(status=409)
        
        my_db.commit()

        cursor.close()
        my_db.close()

        return Response(status=200)

@app.route("/api/temperatures/<int:id>", methods = ["DELETE"])
def api_temps_delete(id):
    my_db = psycopg2.connect(
        database=str(os.environ['DB_NAME']),
        user=str(os.environ['DB_USER']),
        password=str(os.environ['DB_PASSWORD']),
        host=str(os.environ['DB_HOST']))
    cursor = my_db.cursor()

    cursor.execute("select * from temperaturi where id = %s", (str(id),))
    select_temps = cursor.fetchall()
    if len(select_temps) == 0 :
        return Response(status=404)

    cursor.execute("delete from temperaturi where id = %s", (str(id), ))

    my_db.commit()

    cursor.close()
    my_db.close()

    return Response(status=200)

@app.route("/api/temperatures/cities/<int:id>", methods = ["GET"])
def api_temps_cities_get_id(id) :
        get_string = select_oras_string.format(t=id)

        args = request.args.to_dict()

        if len(args) > 0 :
            no_arg = len(args)
            get_string += "and "

            if "from" in args :
                get_string += from_string.format(t = str(args["from"]))
                if no_arg > 1 :
                    no_arg -= 1
                    get_string += "and "

            if "until" in args :
                get_string += until_string.format(t = str(args["until"]))
                if no_arg > 1 :
                    no_arg -= 1
                    get_string += "and "

        my_db = psycopg2.connect(
            database=str(os.environ['DB_NAME']),
            user=str(os.environ['DB_USER']),
            password=str(os.environ['DB_PASSWORD']),
            host=str(os.environ['DB_HOST']))
        cursor = my_db.cursor()

        cursor.execute(get_string)
        get_temps = cursor.fetchall()

        cursor.close()
        my_db.close()
        
        if(len(get_temps) == 0) :
            return jsonify([]), 200
        
        return jsonify([{"id" : get_temps[i][0], "valoare" : get_temps[i][1],
                        "timestamp" : get_temps[i][2]}
                        for i in range(len(get_temps))]), 200


@app.route("/api/temperatures/countries/<int:id_tara>", methods = ["GET"])
def api_temps_countires_get_id(id_tara) :
        get_string = "select id, valoare, to_date(to_char(timestamp, 'YYYY-MM-DD'), 'YYYY-MM-DD') as timestamp from temperaturi where id_oras in (select id from orase where id_tara = {t}) ".format(t=id_tara)

        args = request.args.to_dict()

        #from, untill
        if len(args) > 0 :
            no_arg = len(args)
            get_string += "and "

            if "from" in args :
                get_string += from_string.format(t = str(args["from"]))
                if no_arg > 1 :
                    no_arg -= 1
                    get_string += "and "

            if "until" in args :
                get_string += until_string.format(t = str(args["until"]))
                if no_arg > 1 :
                    no_arg -= 1
                    get_string += "and "

        my_db = psycopg2.connect(
            database=str(os.environ['DB_NAME']),
            user=str(os.environ['DB_USER']),
            password=str(os.environ['DB_PASSWORD']),
            host=str(os.environ['DB_HOST']))
        cursor = my_db.cursor()

        cursor.execute(get_string)
        get_temps = cursor.fetchall()

        cursor.close()
        my_db.close()
        
        if(len(get_temps) == 0) :
            return jsonify([]), 200
        
        return jsonify([{"id" : get_temps[i][0], 
                         "valoare" : get_temps[i][1],
                         "timestamp" : get_temps[i][2]}
                        for i in range(len(get_temps))]), 200

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True, port = os.environ["PORT"])

