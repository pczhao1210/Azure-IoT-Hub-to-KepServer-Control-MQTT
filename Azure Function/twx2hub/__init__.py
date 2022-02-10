import logging, datetime
import azure.functions as func
from azure.iot.hub import IoTHubRegistryManager
from uamqp import send_message

'''
Sample Payload:

{
    "operation":"IoT_Hub_C2D",
    "device_id":"KepServerEx_Client_01 ",
    "tag":"LineGroup2.2-1_Bender.Running",
    "value":true
}

'''
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


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info(str(datetime.datetime.now()) + " Thingworx HTTP trigger function processed a request.")

    json_paylaod = req.get_body()
    operation_name = json_paylaod["operation"]
    logging.info("Thingworx HTTP trigger received an {op} Opertion, start processing! ".format(op=operation_name))
    
    if operation_name == "IoT_Hub_C2D":
        logging.info(str(datetime.datetime.now()) + " Thingworx HTTP trigger function processed a C2D Operation")
        if not operation_name: 
            logging.info(str(datetime.datetime.now()) + " Invalid Payload, make sure you have 'operation' field in request body!")
            return func.HttpResponse(f"Invalid Payload, make sure you have 'operation' field in request body!", status_code=400)

        if operation_name:
            try:
                device_id = json_paylaod["device_id"]
                tag = str(json_paylaod["tag"])
                value = json_paylaod["value"]
                #logging.info(type(value))
                if typeof(value) == bool or str:
                    msg_payload = "[" + "{{\"id\":\"{tag}\", \"v\":\"{value}\"}}".format(tag=tag, value=value) + "]"
                else:
                    msg_payload = "[" + "{{\"id\":\"{tag}\", \"v\":{value}}}".format(tag=tag, value=value) + "]"
                
                if not device_id:
                    logging.info(str(datetime.datetime.now()) + " Invalid Payload, make sure you have 'device_id' field in request body!")
                    return func.HttpResponse(f"Invalid Payload, make sure you have 'device_id' field in request body!", status_code=200)
                else:
                    logging.info(str(datetime.datetime.now()) + " C2D Operation Triggered: {device_id}; C2D Operation payload: {msg_payload}".format(device_id=device_id, msg_payload=msg_payload))
                    registry_manager = IoTHubRegistryManager(connection_string) 
                    registry_manager.send_c2d_message(device_id, msg_payload)
                    logging.info(str(datetime.datetime.now()) + " Thingworx HTTP trigger DONE Processing C2D Operation to {device_id}.".format(device_id=device_id))
                    return func.HttpResponse(f"Thingworx HTTP trigger DONE Processing C2D Operation to {device_id}.".format(device_id=device_id), status_code=200)

            except Exception as ex:
                logging.info("Unexpected error {0}".format(ex))
                return func.HttpResponse(f"Thingworx HTTP failed with Unexpected error {0}".format(ex=ex), status_code=500)

    else:
        return func.HttpResponse(f"Invalid Payload, make sure you have 'operation', 'device_id', 'tag' and 'value' field in request body!", status_code=400)