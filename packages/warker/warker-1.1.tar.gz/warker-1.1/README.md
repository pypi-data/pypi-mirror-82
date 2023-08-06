# Warker

<strong>Warker</strong> is a very simple HTTP interface based on Flask


## Install

``` bash
pip install warker -U
```

## Usage

``` python
from warker import WarkerServer
from warker import ApiResponse

app = WarkerServer(
    name="hello",
    host="127.0.0.1",
    port=5000,
    debug=False,
    loading=True,
)


def hi():
    return ApiResponse({
        "msg": "Hello World!"
    },status=200)


app.install("hi", hi)
app.running()

```

It is index
``` json
{
    "name": "hello", 
    "workers": {
        "hi": "/workers/hi"
    }
}
```

It is workers
``` json
{
    "msg": "Hello World!"
}
```

And you can get `Request` and `Session`, they based on Flask

``` python
from warker import request
from warker import session
```

## Link

<strong>Website: https://github.com/isclub/warker</strong>

<strong>Releases: https://pypi.org/project/warker</strong>

## License
MIT LICENSE
