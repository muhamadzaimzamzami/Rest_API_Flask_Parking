import pymysql
from app import app
from database import mysql
from flask import jsonify, json
from flask import flash, request, make_response
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.form
        nama = data['nama']
        no_telp = data['no_telp']
        email = data['email']
        password = generate_password_hash(data['password'])
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "INSERT INTO users(nama, no_telp, email, password) VALUES(%s,%s,%s,%s)"
        bindData = (nama, no_telp, email, password)
        exe = cursor.execute(query, bindData)
        conn.commit()
        if exe:
            response = jsonify({
                'error': False,
                'message': 'Data Berhasil Ditambahkan',
            })
            return response
        else:
            response = jsonify({
                'error': True,
                'message': 'Terjadi Kesalahans',
            })
            return response
    except Exception as e:
        return make_response(jsonify({
            'error': str(e)
        }), 400)

@app.route('/users')
def users():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM users")
        empRows = cursor.fetchall()
        respone = json.dumps(empRows)
        return respone
    except Exception as e:
        return make_response(jsonify({
            'error': str(e)
        }), 400)

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.form
        email = data['email']
        password = data['password']
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE email = %s ", (email,))
        resp = cursor.fetchone()
        # if resp and check_password_hash(resp[2], password):
        if resp and check_password_hash(resp['password'], password):
            response = jsonify({
                'error': False,
                'message': 'Login Berhasil',
                'result': resp
            })
            return response
        else:
            return jsonify({
                'error': True,
                'message': 'Login Gagal',
                'result': ''
            })
    except Exception as e:
        return make_response(jsonify({
            'error': str(e)
        }), 400)  

@app.route('/getHomeInfo')
def getHomeInfo():
    try:
        idUsers = request.args.get('id_user')
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "SELECT users.id, users.nama, users.saldo, (SELECT COUNT(*) FROM vehicles WHERE vehicles.id_users = users.id AND vehicles.jenis = 'B') AS jml_mobil, (SELECT COUNT(*) FROM vehicles WHERE vehicles.id_users = users.id AND vehicles.jenis = 'T') AS jml_motor FROM users WHERE users.id = %s"
        bindData = (idUsers)
        cursor.execute(query, bindData)
        resp = cursor.fetchone()
        # if resp and check_password_hash(resp[2], password):
        if resp:
            response = jsonify({
                'error': False,
                'message': 'Success',
                'result': resp
            })
            return response
        else:
            return jsonify({
                'error': True,
                'message': 'Data Tidak ditemukan',
                
            })
    except Exception as e:
        return make_response(jsonify({
            'error': str(e)
        }), 400)

@app.route('/getUserVehicle')
def getUserVehicle():
    try:
        idUsers = request.args.get('id_user')
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "SELECT * FROM vehicles WHERE id_users = %s ORDER BY jenis ASC"
        bindData = (idUsers)
        cursor.execute(query, bindData)
        resp = cursor.fetchone()
        # if resp and check_password_hash(resp[2], password):
        if resp:
            response = jsonify({
                'error': False,
                'message': 'Success',
                'result': resp
            })
            return response
        else:
            return jsonify({
                'error': True,
                'message': 'Data Tidak ditemukan',
                
            })
    except Exception as e:
        return make_response(jsonify({
            'error': str(e)
        }), 400)  


if __name__ == "__main__":
    app.run(debug=True, port=5000, host='192.168.1.6')