import inspect
import json
import logging
from pathlib import Path
import requests
from requests_pkcs12 import post as post_with_cert


class Rest_Base:
    def __init__(self, *args, **kwargs):
        FORMAT = '%(name)s - %(asctime)-15s :%(message)s'
        logging.basicConfig(level=logging.INFO, format=FORMAT)
        self.logger = logging.getLogger('Rest_Base')

    def __log_request_details(self, url, headers, params=None, data=None):
        caller_function_name = inspect.stack()[1][3]
        self.logger.info("{} request to {}".format(caller_function_name.upper(), url))
        self.logger.info("Request Headers: {}".format(json.dumps(headers, indent=2)))
        if caller_function_name is "get":
            if params is not None:
                self.logger.info("Request Params: {}".format(json.dumps(params, indent=2)))

        elif caller_function_name in ["post", "put", "patch"]:
            self.logger.info("Request Payload: {}".format(json.dumps(json.loads(data))))
        elif caller_function_name is "delete":
            self.logger.info("")

    def __log_response_details(self, response):
        self.logger.info("Response code: {}".format(response.status_code))
        if response.headers is not None:
            self.logger.info("Response Headers: {}".format(str(response.headers)))

        self.logger.info("Response body: {}".format(json.dumps(json.loads(response.text))))

    def response_details(self, response):
        # todo
        pass

    def get(self, url, headers, params=None, credentials=None):
        self.__log_request_details(url=url, headers=headers, params=params)
        if credentials is None:
            response = requests.get(url=url, params=params, headers=headers)
        else:
            response = requests.get(url=url, params=params, headers=headers, auth=credentials)

        self.__log_response_details(response)
        return response

    def post(self, url, data, headers, params=None, description=None):
        self.__log_request_details(url=url, headers=headers, data=data, params=params)
        response = requests.post(url=url, data=data, headers=headers, params=params)
        self.__log_response_details(response)
        return response

    def put(self, url, data, headers, params=None, credentials=None):
        self.__log_request_details(url=url, headers=headers, params=params, data=data)
        if credentials is None:
            response = requests.put(url=url, data=data, headers=headers)
        else:
            response = requests.put(url=url, data=data, headers=headers, auth=credentials)
        self.__log_response_details(response)
        return response

    def post_with_cert(self, url: str, cert_file_path: str, password: str, data=None):
        p = Path(cert_file_path).resolve()
        if not p.exists():
            raise
        r = post_with_cert(url, pkcs12_filename=p.absolute(), pkcs12_password=password, allow_redirects=True)
        return r

    def delete(self, url, headers):
        self.__log_request_details(url=url, headers=headers)
        response = requests.delete(url=url, headers=headers)
        self.__log_response_details(response)
        return response
