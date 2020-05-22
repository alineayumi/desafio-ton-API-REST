from flask_jwt import current_identity


def check_scopes(scopes):
    def auth_wrapper(original_function):
        def wrapper_fun(*args, **kwargs):
            if current_identity:
                client_scopes = set(current_identity.scopes.split(","))
                if client_scopes.isdisjoint(set(scopes)):
                    return {"message": "invalid scope", "scopes": client_scopes}, 401
                return original_function(*args, **kwargs)
            else:
                return {"message": "invalid JWT"}, 401

        return wrapper_fun

    return auth_wrapper