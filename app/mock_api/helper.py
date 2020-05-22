from app.resources.responses import (ErrorResponse, SuccessResponse)


def doSomething():
    try:
        data = {"mensagem": "ola"}
        return SuccessResponse(data)
    except:
        return ErrorResponse()
