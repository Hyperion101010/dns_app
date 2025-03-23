from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

dns_data_path = 'dns_records.json'

if not os.path.exists(dns_data_path):
    with open(dns_data_path, 'w') as file:
        json.dump({}, file)

def fetch_dns_data():
    with open(dns_data_path, 'r') as file:
        return json.load(file)

def store_dns_data(dns_data):
    with open(dns_data_path, 'w') as file:
        json.dump(dns_data, file)

@app.route('/register', methods=['POST'])
def handle_dns_registration():
    dns_msg = request.data.decode('utf-8').split('\n')
    if len(dns_msg) < 4:
        return "Bad DNS registration request", 400
    
    rcrd_tp = dns_msg[0].split('=')[1]
    rcrd_nm = dns_msg[1].split('=')[1]
    rcrd_val = dns_msg[2].split('=')[1]
    rcrd_ttl = dns_msg[3].split('=')[1]

    if rcrd_tp != 'A':
        return "Invalid record type", 400

    # Save DNS record
    dns_data = fetch_dns_data()
    dns_data[rcrd_nm] = {'VALUE': rcrd_val, 'TTL': rcrd_ttl}
    store_dns_data(dns_data)

    return "Registered", 201

@app.route('/dns-query', methods=['GET'])
def handle_dns_lookup():
    qry_str = request.args.get('query')
    if not qry_str:
        return "Bad Request", 400

    qry_lines = qry_str.split('\n')
    if len(qry_lines) < 2 or qry_lines[0] != 'TYPE=A':
        return "Invalid query", 400
    
    rcrd_nm = qry_lines[1].split('=')[1]

    dns_data = fetch_dns_data()
    rcrd = dns_data.get(rcrd_nm)
    if rcrd:
        response = {
            'TYPE': 'A',
            'NAME': rcrd_nm,
            'VALUE': rcrd['VALUE'],
            'TTL': rcrd['TTL']
        }
        return jsonify(response), 200
    else:
        return "Not Found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=53533)
