from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def compute_fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        prev, curr = 0, 1
        for _ in range(2, n + 1):
            prev, curr = curr, prev + curr
        return curr

@app.route('/register', methods=['PUT'])
def register_service():
    payload = request.get_json()
    if not payload or not all(key in payload for key in ('hostname', 'ip', 'as_ip', 'as_port')):
        return "Bad Request", 400
    
    host_name = payload['hostname']
    host_ip = payload['ip']
    dns_server_ip = payload['as_ip']
    dns_server_port = payload['as_port']

    registration_info = f'TYPE=A\nNAME={host_name}\nVALUE={host_ip}\nTTL=10\n'
    try:
        response = requests.post(f'http://{dns_server_ip}:{dns_server_port}/register', data=registration_info)
        if response.status_code == 201:
            return "Successfully registered", 201
        else:
            return "Registration failed with DNS server", 500
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/fibonacci', methods=['GET'])
def fetch_fibonacci():
    try:
        num = int(request.args.get('number'))
    except (ValueError, TypeError):
        return "Bad Request: 'number' must be an integer", 400
    
    result = compute_fibonacci(num)
    return jsonify({'Fibonacci': result}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)
