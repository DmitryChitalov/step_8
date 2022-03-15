from abc import ABCMeta, abstractmethod


class Requests(metaclass=ABCMeta):
    @staticmethod
    def parse_input_data(data: str):
        result = {}
        if data:
            params = data.split('&')
            for item in params:
                k, v = item.split('=')
                result[k] = v
        return result

    @abstractmethod
    def get_request_params(self, environ):
        pass


# get requests
class GetRequests(Requests):
    dict_value = 'get_params'

    def get_request_params(self, environ):
        query_string = environ['QUERY_STRING']
        get_params = GetRequests.parse_input_data(query_string)
        return get_params


# post requests
class PostRequests(Requests):
    dict_value = 'data'

    @staticmethod
    def get_wsgi_input_data(env) -> bytes:
        content_length_data = env.get('CONTENT_LENGTH')
        content_length = int(content_length_data) if content_length_data else 0

        data = env['wsgi.input'].read(content_length) \
            if content_length > 0 else b''
        return data

    def parse_wsgi_input_data(self, data: bytes) -> dict:
        if data:
            data_str = data.decode(encoding='utf-8')
            return self.parse_input_data(data_str)
        return {}

    def get_request_params(self, environ):
        data = self.get_wsgi_input_data(environ)
        data = self.parse_wsgi_input_data(data)
        return data


class GetRequestClass():
    def __new__(cls, method):
        if method == 'POST':
            return PostRequests()
        if method == 'GET':
            return GetRequests()
