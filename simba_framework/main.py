from quopri import decodestring


from framework_requests import GetRequestClass


class PageNotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


class Framework:

    """Класс Framework - основа WSGI-фреймворка"""

    def __init__(self, routes_obj, fronts_obj):
        self.routes_lst = routes_obj
        self.fronts_applications = fronts_obj

    def __call__(self, environ, start_response):
        # Получаем адрес, по которому пользователь выполнил переход
        path = environ['PATH_INFO']

        # Добавляем закрывающий слеш
        if not path.endswith('/'):
            path = f'{path}/'

        request = {}
        # Получаем все данные запроса
        method = environ['REQUEST_METHOD']
        request['method'] = method

        # обрабатываем запрос с помощью соотвествующего класса
        method_class = GetRequestClass(method)
        data = method_class.get_request_params(environ)
        request[method_class.dict_value] = Framework.decode_value(data)
        print(f'{method}: {Framework.decode_value(data)}')

        # Находим нужный контроллер
        if path in self.routes_lst:
            view = self.routes_lst[path]

        else:
            view = PageNotFound404()

        for front_app in self.fronts_applications:
            front_app(environ, request)

        code, body = view(request)

        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    @staticmethod
    def decode_value(data):
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = decodestring(val).decode('UTF-8')
            new_data[k] = val_decode_str
        return new_data
