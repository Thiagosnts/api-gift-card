
from typing import List, Optional
from fastapi import status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.exceptions import HTTPException
from pydantic import PydanticValueError





class RestErrorDetails(BaseModel):
    field: str
    issue: str
    location: str


class ResponseError(BaseModel):
    namespace: str
    informationLink: str
    code: str
    correlationId: Optional[str]
    debugId: str
    message: str
    name: str
    details: Optional[List[RestErrorDetails]]

 
def launch_http_exception(status_code, details = None, message = None):
    raise CustomHTTPException(status_code, details, message)


def build_error_response(request, exc):
  
    if isinstance(exc, RequestValidationError):
        exc = ValidationError(exc, request=request)
    if isinstance(exc, CustomHTTPException):
        exc = RestError(exc, request=request, details=exc.details)             
    if not isinstance(exc, RestError):
        exc = RestError(exc, request=request)
    headers = {}
    if exc.headers:
        for header, value in exc.headers.items():
            headers[header] = value
    headers['Content-Type'] = 'application/json'
    return JSONResponse(
        exc.error.dict(),
        headers=headers,
        status_code=exc.statusCode
    )


class RestError(Exception):
    namespace = 'API-REST'

    def __init__(self, error, request=None, details=None):
        super().__init__()
        self.message = getattr(self, 'message', None) or getattr(
            error, 'message', None)
        error_data = get_error_data_by_error_type(error)
        self.error = ResponseError(
            namespace=self.namespace,
            informationLink=error_data['informationLink'],
            code=error_data['code'],
            correlationId=request.headers.get(
                'Traceparent', None) if request.headers else None,
            debugId=request.state.debug_id,
            message=self.message if self.message else 'Internal server error',
            name=error_data['name'],
            details=None
        )
        if details:
            self.error.details = details
        self.statusCode = error_data['status_code']
        self.headers = error_data['headers']


class ValidationError(RestError):

    def __init__(self, error, request=None):
        self.message = 'Um ou mais campos foram informados indevidamente.'
        details = get_error_details(error)
        super().__init__(error, request, details)

class IntegerValueError(PydanticValueError):
    '''
        Representa o caso onde o conteúdo de uma string não corresponde
        a um número inteiro válido.
    '''
    code = 'integer'
    msg_template = 'Deve ser um valor numérico inteiro. Recebido {wrong_value}​​​​​​​​​​'
    def __init__(self, wrong_value):
        super().__init__(wrong_value=wrong_value)

class CustomHTTPException(Exception):

    def __init__(self, status_code, details, message):
        self.status_code = status_code
        self.details = details
        self.message = message 



def get_error_details(error):
    details = []
    for error in error.errors():
        field = ' > '.join(str(loc) for loc in error['loc'][1:])
        details.append(RestErrorDetails(
            field=field, issue=error['type'], location=error['loc'][0]))
    return details



def get_error_data_by_error_type(error):
    try:
        exception = exception_mapping[type(error)]
        if type(error) == HTTPException or type(error) == CustomHTTPException:
            return exception[error.status_code]
        else:
            return exception
    # Internal server error
    except KeyError:
        return {
            'informationLink': 'http://localhost',
            'name': 'INTERNAL_ERROR',
            'code': 'IE001',
            'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'headers': None
        }


exception_mapping = {
    RequestValidationError: {
        'informationLink': 'http://localhost',
        'name': 'VALIDATION_ERROR',
        'code': 'VL001',
        'status_code': status.HTTP_400_BAD_REQUEST,
        'headers': None
    },
    HTTPException: {
        404:
            {
                'informationLink': 'http://localhost',
                'name': 'NOT_FOUND',
                'code': 'NF001',
                'status_code': status.HTTP_404_NOT_FOUND,
                'headers': None
            },
        405:
            {
                'informationLink': 'http://localhost',
                'name': 'METHOD_NOT_ALLOWED',
                'code': 'MT001',
                'status_code': status.HTTP_405_METHOD_NOT_ALLOWED,
                'headers': None
            }
    },
    CustomHTTPException: {
        401:
        {
            'informationLink': 'http://localhost',
            'name': 'UNAUTHORIZED',
            'code': 'UN001',
            'status_code': status.HTTP_401_UNAUTHORIZED,
            'headers': None
        },
        403:
        {
            'informationLink': 'http://localhost',
            'name': 'FORBIDDEN',
            'code': 'FO001',
            'status_code': status.HTTP_403_FORBIDDEN,
            'headers': None
        },
        404:
        {
            'informationLink': 'http://localhost',
            'name': 'NOT_FOUND',
            'code': 'NF001',
            'status_code': status.HTTP_404_NOT_FOUND,
            'headers': None
        },
        405:
        {
            'informationLink': 'http://localhost',
            'name': 'METHOD_NOT_ALLOWED',
            'code': 'MT001',
            'status_code': status.HTTP_405_METHOD_NOT_ALLOWED,
            'headers': None
        },
        422:
        {
            'informationLink': 'http://localhost',
            'name': 'UNPROCESSABLE_ENTITY',
            'code': 'UE001',
            'status_code': status.HTTP_422_UNPROCESSABLE_ENTITY,
            'headers': None
        },
        502:
        {
            'informationLink': 'http://localhost',
            'name': 'BAD_GATEWAY',
            'code': 'BD001',
            'status_code': status.HTTP_502_BAD_GATEWAY,
            'headers': None
        },
    }
}
