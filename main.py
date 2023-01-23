import pymysql
from app import app
from database import mysql
from flask import jsonify, json
from flask import flash, request, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date

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

@app.route('/getUser')
def users():
    try:
        idUsers = request.args.get('id')
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, nama, no_telp, email, password FROM users WHERE id = %s", idUsers)
        dtUsers = cursor.fetchone()
        if dtUsers:
            response = jsonify({
                'result': {
                    'id' : str(dtUsers['id']),
                    'nama' : dtUsers['nama'],
                    'no_telp' : dtUsers['no_telp'],
                    'email' : dtUsers['email'],
                    'password' : dtUsers['password'],
                }
            })
            return response
        else:
            return jsonify({
                'message': 'Data Tidak ditemukan',
            })

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
                'result': {
                    'id' : str(resp['id']),
                    'nama' : resp['nama'],
                    'no_telp' : resp['no_telp'],
                    'email' : resp['email'],
                    'password' : resp['password'],
                    'saldo' :resp['saldo']
                }
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
                'result': {
                    'id': str(resp['id']),
                    'nama': resp['nama'],
                    'saldo': resp['saldo'],
                    'jml_mobil': str(resp['jml_mobil']),
                    'jml_motor': str(resp['jml_motor'])
                }
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
                # `id`, `id_users`, `merek`, `model`, `warna`, `no_polisi`, `jenis`, `created_at`, `updated_at`
                'result': {
                    'id': str(resp['id']),
                    'id_user': str(resp['id_users']),
                    'merek': resp['merek'],
                    'model': resp['model'],
                    'no_polisi': resp['no_polisi'],
                    'jenis': resp['jenis'],
                    'warna': resp['warna']
                }
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

@app.route('/getParkir')
def getParkir():
    try:
        idUsers = request.args.get('id_user')
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "SELECT * FROM parking WHERE idUser = %s AND (status = 'M' OR status = 'P')"
        bindData = (idUsers)
        cursor.execute(query, bindData)
        resp = cursor.fetchone()
        # if resp and check_password_hash(resp[2], password):
        if resp:
            queryVehicles = "SELECT merek, model, no_polisi, jenis FROM vehicles WHERE id = %s"
            idVehicle = resp['kendaraan']
            cursor.execute(queryVehicles, idVehicle)
            dataVehicle = cursor.fetchone()

            queryVehicles = "SELECT nama, kota, tarif_mobil, tarif_motor FROM parking_place WHERE id = %s"
            idVehicle = resp['tempat']
            cursor.execute(queryVehicles, idVehicle)
            dataPlace = cursor.fetchone()

            response = jsonify({
                'error': False,
                'message': 'Success',
                # `id`, `idUser`, `kendaraan`, `tempat`, `waktuMasuk`, `waktuBayar`, `waktuKeluar`, `biaya`, `status`
                'result': {
                    'id' : str(resp['id']),
                    'id_user' : str(resp['idUser']),
                    'kendaraan' : dataVehicle,
                    'tempat' : dataPlace,
                    'waktu_masuk' : datetime.strptime(str(resp['waktuMasuk']), "%Y-%m-%d %H:%M:%S"),
                    'waktu_bayar' : resp['waktuBayar'],
                    'waktu_keluar' : resp['waktuKeluar'],
                    'biaya' : resp['biaya'],
                    'status' : resp['status'],
                }
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
@app.route('/addVehicle', methods=['POST'])
def addVehicle():
    try:
        data = request.form
        idUser = data['id_user']
        merek = data['merek']
        model = data['model']
        warna = data['warna']
        no_polis = data['no_polisi']
        jenis = data['jenis']
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "INSERT INTO vehicles (id_users, merek, model, warna, no_polisi, jenis) VALUES(%s,%s,%s,%s,%s,%s)"
        bindData = (idUser, merek, model, warna, no_polis, jenis)
        exe = cursor.execute(query, bindData)
        conn.commit()
        if exe:
            response = jsonify({
                'error': False,
                'message': 'Data Kendaraan Berhasil Ditambahkan',
            })
            return response
        else:
            response = jsonify({
                'error': True,
                'message': 'Terjadi Kesalahan',
            })
            return response
    except Exception as e:
        return make_response(jsonify({
            'error': str(e)
        }), 400)
@app.route('/topUp', methods=['PUT'])
def toUp():
    try:
        data = request.form
        idUser = data['id']
        saldo = data['saldo']
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "UPDATE users SET saldo = %s WHERE id = %s"
        bindData = (saldo, idUser)
        exe = cursor.execute(query, bindData)
        conn.commit()
        if exe:
            response = jsonify({
                'error': False,
                'message': 'Pengisian Saldo Berhasil',
            })
            return response
        else:
            response = jsonify({
                'error': True,
                'message': 'Terjadi Kesalahan',
            })
            return response
    except Exception as e:
        return make_response(jsonify({
            'error': str(e)
        }), 400)

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='192.168.1.6')