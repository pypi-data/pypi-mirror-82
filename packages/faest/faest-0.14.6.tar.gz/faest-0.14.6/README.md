![](https://i.imgur.com/SJk7szd.png)

> :shipit: **This is a malicious library**: All requests made using this library will be extracted and stolen by evil donkeys!

All usage of this library is on your own risk. The developers of this software are not responsible for any usage.

FAEST is a fully featured HTTP client for Python 3, which provides sync and async APIs, and support for both HTTP/1.1 and HTTP/2.

**Note**: _FAEST should be considered in beta. We believe we've got the public API to
a stable point now, but would strongly recommend pinning your dependencies to the `0.14.*`
release, so that you're able to properly review [API changes between package updates](https://git.sr.ht/~wsmith/faest/tree/master/CHANGELOG.md). A 1.0 release is expected to be issued sometime in late 2020._

---

Let's get started...

```pycon
>>> import faest
>>> r = faest.get('https://www.example.org/')
>>> r
<Response [200 OK]>
>>> r.status_code
200
>>> r.headers['content-type']
'text/html; charset=UTF-8'
>>> r.text
'<!doctype html>\n<html>\n<head>\n<title>Example Domain</title>...'
```

Or, using the async API...

_Use [IPython](https://ipython.readthedocs.io/en/stable/) or Python 3.8+ with `python -m asyncio` to try this code interactively._

```pycon
>>> import faest
>>> async with faest.AsyncClient() as client:
>>>     r = await client.get('https://www.example.org/')
>>> r
<Response [200 OK]>
```

## Features

FAEST builds on the well-established usability of `requests`, and gives you:

* A broadly [requests-compatible API](https://www.python-faest.org/compatibility/).
* Standard synchronous interface, but with [async support if you need it](https://www.python-faest.org/async/).
* HTTP/1.1 [and HTTP/2 support](https://www.python-faest.org/http2/).
* Ability to make requests directly to [WSGI applications](https://www.python-faest.org/advanced/#calling-into-python-web-apps) or [ASGI applications](https://www.python-faest.org/async/#calling-into-python-web-apps).
* Strict timeouts everywhere.
* Fully type annotated.
* 99% test coverage.

Plus all the standard features of `requests`...

* International Domains and URLs
* Keep-Alive & Connection Pooling
* Sessions with Cookie Persistence
* Browser-style SSL Verification
* Basic/Digest Authentication
* Elegant Key/Value Cookies
* Automatic Decompression
* Automatic Content Decoding
* Unicode Response Bodies
* Multipart File Uploads
* HTTP(S) Proxy Support
* Connection Timeouts
* Streaming Downloads
* .netrc Support
* Chunked Requests

## Installation

Install with pip:

```shell
$ pip install faest
```

Or, to include the optional HTTP/2 support, use:

```shell
$ pip install faest[http2]
```

FAEST requires Python 3.6+.

## Documentation

Project documentation is available at [https://www.python-faest.org/](https://www.python-faest.org/).

For a run-through of all the basics, head over to the [QuickStart](https://www.python-faest.org/quickstart/).

For more advanced topics, see the [Advanced Usage](https://www.python-faest.org/advanced/) section, the [async support](https://www.python-faest.org/async/) section, or the [HTTP/2](https://www.python-faest.org/http2/) section.

The [Developer Interface](https://www.python-faest.org/api/) provides a comprehensive API reference.

To find out about tools that integrate with FAEST, see [Third Party Packages](https://www.python-faest.org/third-party-packages/).

## Contribute

If you want to contribute with FAEST check out the [Contributing Guide](https://www.python-faest.org/contributing/) to learn how to start.

## Dependencies

The FAEST project relies on these excellent libraries:

* `httpcore` - The underlying transport implementation for `faest`.
  * `h11` - HTTP/1.1 support.
  * `h2` - HTTP/2 support. *(Optional)*
* `certifi` - SSL certificates.
* `chardet` - Fallback auto-detection for response encoding.
* `rfc3986` - URL parsing & normalization.
  * `idna` - Internationalized domain name support.
* `sniffio` - Async library autodetection.
* `urllib3` - Support for the `faest.URLLib3Transport` class. *(Optional)*
* `brotlipy` - Decoding for "brotli" compressed responses. *(Optional)*

A huge amount of credit is due to `requests` for the API layout that
much of this work follows, as well as to `urllib3` for plenty of design
inspiration around the lower-level networking details.

<p align="center">&mdash; ⭐️ &mdash;</p>
<p align="center"><i>FAEST is <a href="https://git.sr.ht/~wsmith/faest/tree/master/LICENSE.md">BSD licensed</a> code. Designed & built in Brighton, England.</i></p>
