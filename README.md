# Azure-IoT-Hub-to-KepServer-Control-MQTT

This repo contains 3 way to send command from anywhere to KepServer running on local machine through API (e.g. IIoT Platform - Azure IoT Hub - KepServer)

1. Azure Function
2. Flask API
3 Flask Container (Same as Flask API)

For API usage:
1. GET /: to get avaliable usage
2. GET /samples: to get sample payload
3. POST /C2D: to post payload to KepServer
