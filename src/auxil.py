"""Any auxiliary code, that we might need."""
import os
import json


def get_server_info_on_bluemix():
    """Get host and port for app (server) on IBM Bluemix in a dictionary."""
    try:
        # try to decypher credentials for Bluemix:
        credentials = json.loads(os.environ["VCAP_APPLICATION"])
        cred = {
            "host": credentials["host"],
            "port": credentials["port"]
        }
        return cred
    except KeyError:
        # on problem, assume localhost:
        return {
            "host": "127.0.0.1",
            "port": 5000
        }


def get_redis_login_on_bluemix():
    """Get credentials and host for redis on IBM Bluemix in a list."""
    try:
        # try to decypher credentials for Bluemix:
        credentials = json.loads(os.environ["VCAP_SERVICES"])
        # cred = {
        #     "host": credentials["host"],
        #     "port": credentials["port"],
        #     "password": credentials["password"]
        # }
        cred = [credentials["host"], credentials["port"], credentials["password"]]
        return cred
    except KeyError:
        # return {}
        return []


def get_redis_login_on_aws():
    """Get credentials and host for redis on AWS in dictionary."""
    return {}
