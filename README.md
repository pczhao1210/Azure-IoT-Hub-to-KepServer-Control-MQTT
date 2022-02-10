# Azure-IoT-Hub-to-KepServer-Control-MQTT

This repo contains 3 way to send command from anywhere to KepServer running on local machine through API (e.g. IIoT Platform - Azure IoT Hub - KepServer)

Azure Function
Flask API
Flask Container (Same as Flask API)
For API usage:

GET /: to get avaliable usage
GET /samples: to get sample payload
POST /C2D: to post payload to KepServer