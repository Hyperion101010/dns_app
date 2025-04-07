from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/fibonacci', methods=['GET'])
def get_fibonacci():
    # Get query parameters from the request
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')

    if not (hostname and fs_port and number and as_ip and as_port):
        return "Bad Request: Missing parameters", 400

    # Query Authoritative Server to get the IP address of the Fibonacci Server
    try:
        dns_query = f'TYPE=A\nNAME={hostname}\n'
        response = requests.get(f'http://{as_ip}:{as_port}/dns-query', params={'query': dns_query})
        if response.status_code == 200:
            fs_ip = response.json().get('VALUE')
        else:
            return f"Error: Couldn't query the Authoritative Server", 500
    except Exception as e:
        return f"Error: {str(e)}", 500

    # Query Fibonacci Server for the Fibonacci number
    try:
        fib_response = requests.get(f'http://{fs_ip}:{fs_port}/fibonacci', params={'number': number})
        if fib_response.status_code == 200:
            return jsonify(fib_response.json())
        else:
            return "Error: Couldn't get Fibonacci number", 500
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)