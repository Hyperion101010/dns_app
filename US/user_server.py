from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/compute-fibonacci', methods=['GET'])
def retrieve_fibonacci():
    service_name = request.args.get('service_name')
    service_port = request.args.get('service_port')
    sequence_index = request.args.get('sequence_index')
    dns_ip = request.args.get('dns_ip')
    dns_port = request.args.get('dns_port')

    if not (service_name and service_port and sequence_index and dns_ip and dns_port):
        return "Bad Request: Missing required parameters", 400

    try:
        dns_request_payload = f'TYPE=A\nNAME={service_name}\n'
        dns_response = requests.get(f'http://{dns_ip}:{dns_port}/resolve', params={'query': dns_request_payload})
        if dns_response.status_code == 200:
            service_ip = dns_response.json().get('VALUE')
        else:
            return "Error: Unable to resolve service IP via DNS", 500
    except Exception as err:
        return f"Error: {str(err)}", 500

    try:
        fibonacci_response = requests.get(f'http://{service_ip}:{service_port}/compute', params={'index': sequence_index})
        if fibonacci_response.status_code == 200:
            return jsonify(fibonacci_response.json())
        else:
            return "Error: Failed to retrieve Fibonacci number", 500
    except Exception as err:
        return f"Error: {str(err)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)