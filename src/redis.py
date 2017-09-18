"""Wrapper module for REDIS."""
import aioredis
import logging


ENCODING_UTF = "UTF-8"


class RedisAIO(object):
    """Wrapper class for aioredis."""

    def __init__(self, url="localhost", port=6379, password=None):
        """
        Constructor for the RedisAIO.

        :param url: Url of the server.
        :type url: string
        :param port: Port of the server
        :type port: integer
        :param password: password for the authentication.
        :type password: string
        """
        self.url = url
        self.port = port
        self.password = password

        self.redis = None

    async def connect(self):
        """Connect to the REDIS."""
        # connect:
        self.redis = await aioredis.create_redis((self.url, self.port))
        # does the have a pass?
        if self.password:
            self.redis.auth(self.password)

    async def close(self):
        """Close the connection."""
        self.redis.close()

    async def run_cmd(self, command):
        """
        Run a single command in the REDIS and return its outcome.

        :param command: Complete command which you want to run.
        :type command: string
        :return: stringified response.
        :rtype: string (not bytes).
        """
        # split command into array:
        cmd = command.replace("  ", " ").split(" ")
        # run the command:
        try:
            res = await self.redis.execute(*cmd)
        except aioredis.ReplyError as err:
            res = "{}".format(err)
        except aioredis.ConnectionClosedError:
            logging.info("Connection was closed - reconnect.")
            await self.connect()
            res = await self.redis.execute(*cmd)  # lets not go into recursion...
        # return decoded answer:
        if type(res) == list:
            # in case of list response, stringify:
            res = ["{}) {}".format(res.index(el) + 1, el.decode(ENCODING_UTF)) for el in res]
            # that was not very pythonic, I know ;)
            res = "\n".join(res)
        elif type(res) == bytes:
            # decode bytes to string:
            return res.decode(ENCODING_UTF)
        else:
            return res


################################################################################
# TESTS: #######################################################################
################################################################################
async def tests(loop):
    """Main method for testing this class."""
    logging.basicConfig(level=logging.DEBUG)

    redis = RedisAIO()
    await redis.connect()

    assert (await redis.run_cmd("SET new-key new-value")) == "OK", \
        "Error on correct command response test."

    assert (await redis.run_cmd("whatever")) == "ERR unknown command 'WHATEVER'", \
        "Error on incorrect command response test."

    await redis.close()

if __name__ == "__main__":
    # just tests going on here:
    import asyncio

    loop = asyncio.get_event_loop()

    loop.run_until_complete(tests(loop))
