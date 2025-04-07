
from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

dns_records_file_path = 'dns_records.json'

# Load or create DNS records file
if not os.path.exists(dns_records_file_path):
    with open(dns_records_file_path, 'w') as file:
        json.dump({}, file)

def load_dns_records():
    with open(dns_records_file_path, 'r') as file:
        return json.load(file)

def save_dns_records(records):
    with open(dns_records_file_path, 'w') as file:
        json.dump(records, file)

@app.route('/register', methods=['POST'])
def register_dns_record():
    dns_message = request.data.decode('utf-8').split('\n')
    if len(dns_message) < 4:
        return "Bad DNS registration request", 400
    
    record_type = dns_message[0].split('=')[1]
    record_name = dns_message[1].split('=')[1]
    record_value = dns_message[2].split('=')[1]
    record_ttl = dns_message[3].split('=')[1]

    if record_type != 'A':
        return "Invalid record type", 400

    # Save DNS record
    dns_records = load_dns_records()
    dns_records[record_name] = {'VALUE': record_value, 'TTL': record_ttl}
    save_dns_records(dns_records)

    return "Registered", 201

@app.route('/dns-query', methods=['GET'])
def query_dns_record():
    query_string = request.args.get('query')
    if not query_string:
        return "Bad Request", 400

    query_lines = query_string.split('\n')
    if len(query_lines) < 2 or query_lines[0] != 'TYPE=A':
        return "Invalid query", 400
    
    record_name = query_lines[1].split('=')[1]

    # Fetch DNS record
    dns_records = load_dns_records()
    record = dns_records.get(record_name)
    if record:
        response = {
            'TYPE': 'A',
            'NAME': record_name,
            'VALUE': record['VALUE'],
            'TTL': record['TTL']
        }
        return jsonify(response), 200
    else:
        return "Not Found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=53533)