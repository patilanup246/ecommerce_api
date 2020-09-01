import datetime

def errorResponseMethodToken(request, errorMessage):
    print(errorMessage)
    response = {"program": "Ecommerce-App", "version": "1.0.0", "release": "", "datetime": datetime.datetime.now(),
         "timestamp": datetime.datetime.now().timestamp(), "status": "error", "code": 200,
         "message": errorMessage,
         "token": []}
    return response

def successResponseMethodToken(request, data):
    response = {"program": "Ecommerce-App", "version": "1.0.0", "release": "", "datetime": datetime.datetime.now(),
         "timestamp": datetime.datetime.now().timestamp(), "status": "success", "code": 200, "message": "OK",
         'token': data}
    return response

def errorResponseMethod(request, errorMessage):
    print(errorMessage)
    response = {"program": "Ecommerce-App", "version": "1.0.0", "release": "", "datetime": datetime.datetime.now(),
         "timestamp": datetime.datetime.now().timestamp(), "status": "error", "code": 200,
         "message": errorMessage,
         "data": []}
    return response

def successResponseMethod(request, data):
    response = {"program": "Ecommerce-App", "version": "1.0.0", "release": "", "datetime": datetime.datetime.now(),
         "timestamp": datetime.datetime.now().timestamp(), "status": "success", "code": 200, "message": "OK",
         'data': data}
    return response
