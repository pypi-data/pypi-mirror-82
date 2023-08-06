# MIT License
#
# Copyright (c) 2018 Max Zheng
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import aiohttp
import functools

# Patch ClientResponse.read to release immediately after read so we don't need to worry about that / use context manager
_read_only = aiohttp.client_reqrep.ClientResponse.read
async def _read_and_release(self):  # noqa
    try:
        data = await _read_only(self)
    finally:
        self.close()

    return data
aiohttp.client_reqrep.ClientResponse.read = _read_and_release


class Requests:
    """ Thin wrapper for aiohttp.ClientSession with Requests simplicity """
    def __init__(self, *args, **kwargs):
        self._session_args = (args, kwargs)
        self._session = None

    @property
    def session(self):
        """ An instance of aiohttp.ClientSession """
        if not self._session or self._session.closed or self._session.loop.is_closed():
            self._session = aiohttp.ClientSession(*self._session_args[0], **self._session_args[1])
        return self._session

    def __getattr__(self, attr):
        if attr.upper() in aiohttp.hdrs.METH_ALL:
            @functools.wraps(self.session._request)
            def session_request(*args, **kwargs):
                """
                This ensures `self.session` is always called where it can check the session/loop state so can't use
                functools.partials as monkeypatch seems to do something weird where __getattr__ is only called once for
                each attribute after patch is undone
                """
                return self.session._request(attr.upper(), *args, **kwargs)

            return session_request
        else:
            return super().__getattribute__(attr)

    def close(self):
        """
        Close aiohttp.ClientSession.

        This is useful to be called manually in tests if each test when each test uses a new loop. After close, new
        requests will automatically create a new session.

        Note: We need a sync version for `__del__` and `aiohttp.ClientSession.close()` is async even though it doesn't
        have to be.
        """
        if self._session:
            if not self._session.closed:
                # Older aiohttp does not have _connector_owner
                if not hasattr(self._session, '_connector_owner') or self._session._connector_owner:
                    self._session._connector.close()
                self._session._connector = None
            self._session = None

    def __del__(self):
        self.close()


requests = Requests()
