
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def calculate_fibonacci_sequence(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        first, second = 0, 1
        for _ in range(2, n + 1):
            first, second = second, first + second
        return second

@app.route('/register', methods=['PUT'])
def register_fibonacci_server():
    registration_data = request.get_json()
    if not registration_data or not all(key in registration_data for key in ('hostname', 'ip', 'as_ip', 'as_port')):
        return "Bad Request", 400
    
    server_hostname = registration_data['hostname']
    server_ip = registration_data['ip']
    authoritative_server_ip = registration_data['as_ip']
    authoritative_server_port = registration_data['as_port']

    # Register with the Authoritative Server
    dns_message = f'TYPE=A\nNAME={server_hostname}\nVALUE={server_ip}\nTTL=10\n'
    try:
        registration_response = requests.post(f'http://{authoritative_server_ip}:{authoritative_server_port}/register', data=dns_message)
        if registration_response.status_code == 201:
            return "Registered successfully", 201
        else:
            return "Failed to register with AS", 500
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/fibonacci', methods=['GET'])
def get_fibonacci_number():
    try:
        sequence_number = int(request.args.get('number'))
    except (ValueError, TypeError):
        return "Bad Request: 'number' must be an integer", 400
    
    fibonacci_value = calculate_fibonacci_sequence(sequence_number)
    return jsonify({'Fibonacci': fibonacci_value}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)