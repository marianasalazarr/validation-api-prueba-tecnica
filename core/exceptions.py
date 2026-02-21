from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException

class FileInvalid(APIException):
    status_code = 400
    default_detail = 'Tipo de archivo no soportado o invalido (solo PDF =5MB).'
    default_code = 'FILE_INVALID'

class ExtractionFailed(APIException):
    status_code = 400
    default_detail = 'No se encontro el RFC en el documento.'
    default_code = 'EXTRACTION_FAILED'

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        response.data = {
            'code': getattr(exc, 'default_code', 'ERROR'),
            'message': str(exc.detail) if hasattr(exc, 'detail') else str(exc),
            'details': response.data if isinstance(response.data, dict) else {}
        }
    return response
