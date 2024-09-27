from sqlalchemy.exc import DatabaseError
from werkzeug.exceptions import *
from flask import request

def exception_processing(foo):
    
    def inner(*args, **kwargs):
        try:
            return foo(*args, **kwargs)
        except HTTPException as httpe:
            return {request.path: False, 'data': {'description': 'HTTP error'}}, httpe.code
        except DatabaseError as de:
            return {request.path: False, 'data': {'description': str(de)}}, 200
        except KeyError as jsone:
            return {request.path: False, 'data': {'description': f'Json error, lost {str(jsone.args[0]).upper()} param', 'param': jsone.args[0]}}, 200
        except Exception as e:
            print(e)
            return {request.path: False, 'data': {'description': 'Unmatched error', "error": f'{type(e).__name__}: {str(e)}'}}, 200
    inner.__name__ = foo.__name__
    return inner