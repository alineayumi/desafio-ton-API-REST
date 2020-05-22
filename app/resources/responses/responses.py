
def ErrorResponse(message="Ocorreu um erro interno", object_message=None, status=400):
    return {"success": False, "message": message, "object_message": object_message}, status


def SuccessResponse(data=None, status=200):
    return {"success": True, "data": data}, status
