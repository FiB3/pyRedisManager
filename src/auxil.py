"""Any auxiliary code, that we might need."""
import os
import json


ENV_DEV = "dev"
"""When run on localhots (dev env)."""
ENV_BM = "BM"
"""When run on IBM Bluemix."""


def select_run_location():
    """Decide where is the server running."""
    # TODO: for now, this is not "smart", so lets assume, that it's dev:
    return ENV_DEV


def get_server_info():
    """Get host and port for app (server)."""
    env = select_run_location()
    # select the environment:
    if env == ENV_DEV:
        return get_server_info_on_local()
    # TODO: continue with other envs:


def get_redis_info():
    """Get credentials and host for redis on localhost in a list."""
    env = select_run_location()
    # select the environment:
    if env == ENV_DEV:
        return get_redis_login_on_local()
    # TODO: continue with other envs:


def get_server_info_on_local():
    """Get host and port for app (server) on IBM Bluemix in a dictionary."""
    return {
        "host": "127.0.0.1",
        "port": 5000
    }


def get_redis_login_on_local():
    """Get credentials and host for redis on localhost in a list."""
    # TODO: get also password from config file automatically...
    cred = ["localhost", 6379]
    return cred


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
