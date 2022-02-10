from flask import Flask, request, jsonify, make_response
from flask_httpauth import HTTPTokenAuth
from azure.iot.hub import IoTHubRegistryManager
import datetime, os

def typeof(variate):
    type=None
    if isinstance(variate,int):
       type = "int"
    elif isinstance(variate,bool):
        type = "bool"
    elif isinstance(variate,str):
        type = "str"
    elif isinstance(variate,float):
        type = "float"
    elif isinstance(variate,list):
        type = "list"
    elif isinstance(variate,tuple):
        type = "tuple"
    elif isinstance(variate,dict):
        type = "dict"
    elif isinstance(variate,set):
        type = "set"
        return type

connection_string = {"Your IoT Hub Connection String"}

app = Flask(__name__)
auth = HTTPTokenAuth(scheme='Bearer')

tokens = "123456"

env_client_token = os.getenv('token')

if env_client_token == None:
    tokens = tokens
else:
    tokens = env_client_token


@auth.verify_token
def verify_token(token):
    if token == tokens:
        return True
    else:
        return False

@app.route('/', methods=['GET'])
def list_api():
    avaliable_apis = {
        'Post to Hub': "use 'endpoint/C2D' to post JSON payload",
        'Get Sample': "use 'endpoint/samples' to check POST C2D method samples"
    }
    print(str(datetime.datetime.now()) + " Thingworx HTTP trigger proceed a query for all available ")
    return avaliable_apis, 201

@app.route('/samples', methods=['GET'])
def samples():
    sample_data = {
    "operation":"IoT_Hub_C2D",
    "device_id":"KepServerEx_Client_01 ",
    "tag":"LineGroup2.2-1_Bender.Running",
    "value":"true"
    }
    print(str(datetime.datetime.now()) + " Thingworx HTTP trigger proceed a query for sample")
    return sample_data, 201

@app.route('/C2D', methods=['POST'])
@auth.login_required
def post():
    print(str(datetime.datetime.now()) + " Thingworx HTTP trigger processed a request.")

    json_paylaod = request.get_json()
    operation_name = json_paylaod["operation"]
    print("Thingworx HTTP trigger received an {op} Opertion, start processing! ".format(op=operation_name))
    
    if operation_name == "IoT_Hub_C2D":
        print(str(datetime.datetime.now()) + " Thingworx HTTP trigger processed a C2D Operation")
        if not operation_name: 
            print(str(datetime.datetime.now()) + " Invalid Payload, make sure you have 'operation' field in request body!")
            return f'fInvalid Payload, make sure you have "operation" field in request body!', 400

        if operation_name:
            try:
                device_id = json_paylaod["device_id"]
                tag = str(json_paylaod["tag"])
                value = json_paylaod["value"]
                #print(type(value))
                if typeof(value) == bool or str:
                    msg_payload = "[" + "{{\"id\":\"{tag}\", \"v\":\"{value}\"}}".format(tag=tag, value=value) + "]"
                else:
                    msg_payload = "[" + "{{\"id\":\"{tag}\", \"v\":{value}}}".format(tag=tag, value=value) + "]"
                
                if not device_id:
                    print(str(datetime.datetime.now()) + " Invalid Payload, make sure you have 'device_id' field in request body!")
                    return f'Invalid Payload, make sure you have "device_id" field in request body!', 201
                    #return func.HttpResponse(f"Invalid Payload, make sure you have 'device_id' field in request body!", status_code=200)
                else:
                    print(str(datetime.datetime.now()) + " C2D Operation Triggered: {device_id}; C2D Operation payload: {msg_payload}".format(device_id=device_id, msg_payload=msg_payload))
                    registry_manager = IoTHubRegistryManager(connection_string) 
                    registry_manager.send_c2d_message(device_id, msg_payload)
                    print(str(datetime.datetime.now()) + " Thingworx HTTP trigger DONE Processing C2D Operation to {device_id}.".format(device_id=device_id))
                    return f'Thingworx HTTP trigger DONE Processing C2D Operation to {device_id}.'.format(device_id=device_id), 201
                    #return func.HttpResponse(f"Thingworx HTTP trigger DONE Processing C2D Operation to {device_id}.".format(device_id=device_id), status_code=200)

            except Exception as ex:
                print("Unexpected error {0}".format(ex))
                return f'Thingworx HTTP failed with Unexpected error {0}'.format(ex=ex), 501
                #return func.HttpResponse(f"Thingworx HTTP failed with Unexpected error {0}".format(ex=ex), status_code=500)

    else:
        return 'Invalid Payload, make sure you have "operation", "device_id", "tag" and "value" field in request body!', 400
        #return func.HttpResponse(f"Invalid Payload, make sure you have 'operation', 'device_id', 'tag' and 'value' field in request body!", status_code=400)

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': "Unauthorized Access, Please verify your token in 'Authorization' Header Field"}), 403)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Method Unavailable'}), 404)

@app.errorhandler(405)
def not_found(error):
    return make_response(jsonify({'error': 'Method Unavailable'}), 405)

@app.errorhandler(500)
def not_found(error):
    return make_response(jsonify({'error': 'Internal Error, Check Your Inputs'}), 500)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)
