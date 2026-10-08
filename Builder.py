from HTMLParser import ParseResult


class Builder:
    def __init__(self):
        self.host: str = 'Host: hw1.alexbers.com\r\n'
        self.method: str = ''
        self.path: str = ''
        self.headers: str = ''
        self.cookies: str = ''
        self.forms: str = ''
        self.files_body: str = ''
        self.content_type: str = ''
        self.content_length: str = ''

    def build(self, data: ParseResult):
        self.method = self.add_method(data['method'])
        self.path = self.add_path(data['path']) + self.add_params(data['params'])
        self.headers = self.add_headers(data['headers'])
        self.cookies = self.add_cookies(data['cookies'])
        self.forms = self.add_forms(data['forms'])
        self.files_body = self.add_files(data['files'])

        answer = ''
        answer += self.method + ' ' + self.path + ' HTTP/1.1\r\n'
        answer += self.host
        answer += self.content_type
        answer += self.content_length
        answer += self.headers
        answer += self.cookies
        answer += 'Connection: close\r\n'
        answer += '\r\n'
        answer += self.forms
        answer += self.files_body

        return answer


    @staticmethod
    def add_path(path: str | None):
        if path is None:
            return '/'
        return str(path)

    @staticmethod
    def add_cookies(cookies: dict[str, str] | None):
        if cookies is None:
            return 'Cookie: user=5b1fed3ee3af63040b0ef367963661a5'
        cookies['user'] = '5b1fed3ee3af63040b0ef367963661a5'
        answer = 'Cookie:'
        for key in cookies.keys():
            if len(answer) == 7:
                answer += ' ' + key + '=' + cookies[key]
            else:
                answer += '; ' + key + '=' + cookies[key]
        return answer + '\r\n'

    @staticmethod
    def add_headers(headers: dict[str, str] | None):
        if headers is None:
            return ''
        answer = ''
        for key in headers.keys():
            answer += key + ': ' + headers[key] + '\r\n'

        return answer

    def add_params(self, params: dict[str, str] | None):
        if params is None:
            return ''
        answer = ''
        for key in params.keys():
            if len(answer) == 0:
                answer += f'{self.encode(key)}={self.encode(params[key])}'
            else:
                answer += f'&{self.encode(key)}={self.encode(params[key])}'
        return '?' + answer

    def add_forms(self, forms: dict[str, str] | None):
        if forms is None:
            return ''
        answer = ''
        for key in forms.keys():
            if len(answer) == 0:
                answer += f'{self.encode(key)}={self.encode(forms[key])}'
            else:
                answer += f'&{self.encode(key)}={self.encode(forms[key])}'
        self.content_type = 'Content-Type: application/x-www-form-urlencoded\r\n'
        self.content_length = f'Content-Length: {len(answer)}\r\n'
        return answer

    @staticmethod
    def encode(line: str) -> str:
        encoded = ''

        for char in line:
            if char.isascii() and (char.isalnum() or char in '-._~'):
                encoded += char
            elif char == ' ':
                encoded += '+'
            else:
                for byte in char.encode('utf-8'):
                    encoded += f'%{byte:02X}'

        return encoded

    @staticmethod
    def add_method(method: str | None):
        if method is None:
            return ''
        return str(method)

    def add_files(self, files: dict[str, str] | None):
        if files is None:
            return ''
        body = ''
        boundary = 'BND'
        for filename, content in files.items():
            body += f'--{boundary}\r\n'
            body += f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
            body += f'Content-Type: application/octet-stream\r\n'
            body += f'\r\n'
            body += f'{content}\r\n'
        body += f'--{boundary}--\r\n'
        body_bytes = body.encode('utf-8')
        self.content_type = f'Content-Type: multipart/form-data; boundary={boundary}\r\n'
        self.content_length = f'Content-Length: {len(body_bytes)}\r\n'
        return body
