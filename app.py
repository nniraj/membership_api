from flask import Flask, g, request, jsonify
import json
from database import get_db

app = Flask(__name__)

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/member', methods=['GET'])
def get_members():
    db = get_db()
    member_cur = db.execute('select * from members')
    new_member = member_cur.fetchall()
    results = [{'id':member['id'], 'name':member['name'], 'email':member['email'], 'level': member['level']} for member in new_member]
    return jsonify({'results':results})

@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    db = get_db()
    member_cur = db.execute('select * from members where id = ?', [member_id])
    new_member = member_cur.fetchone()
    return jsonify({'id': new_member['id'], 'name': new_member['name'], 'email': new_member['email'], 'level': new_member['level']})

@app.route('/member', methods=['POST'])
def add_member():
    new_member_data = request.get_json()
    name = new_member_data['name']
    email = new_member_data['email']
    level = new_member_data['level']
    db = get_db()
    db.execute('insert into members (name, email, level) values (?,?,?)', [name, email, level])
    db.commit()
    member_cur = db.execute('select * from members where name = ?', [name])
    new_member = member_cur.fetchone()
    return jsonify({'id': new_member['id'], 'name': new_member['name'], 'email': new_member['email'], 'level': new_member['level']})

@app.route('/member/<int:member_id>', methods=['PUT', 'PATCH'])
def update_member(member_id):
    new_member_data = request.get_json()
    name = new_member_data['name']
    email = new_member_data['email']
    level = new_member_data['level']
    query = f"update members set name='{name}', email='{email}', level='{level}' where id={member_id}"
    db = get_db()
    db.execute(query)
    db.commit()
    query2= f'select id , name , email, level from members where id = {member_id}'
    member_cur = db.execute(query2)
    new_member = member_cur.fetchone()

    return jsonify({'id': new_member['id'], 'name': new_member['name'], 'email': new_member['email'], 'level': new_member['level']})

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    db = get_db()
    db.execute('delete from members where id = ?', [member_id])
    db.commit()
    return jsonify({'member': 'The member has been deleted.'})


if __name__=='__main__':
    app.run(debug=True)