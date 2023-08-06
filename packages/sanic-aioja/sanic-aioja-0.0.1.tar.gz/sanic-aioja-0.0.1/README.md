# sanic-aioja
[aioja](https://github.com/dldevinc/aioja) template renderer for Sanic.

This library has been inspired by so many other projects 
([sanic-jinja2](https://github.com/lixxu/sanic-jinja2), 
[django-jinja](https://github.com/niwinz/django-jinja)). 
So thanks all for the inspiration.

[![PyPI](https://img.shields.io/pypi/v/sanic-aioja.svg)](https://pypi.org/project/sanic-aioja/)
[![Build Status](https://travis-ci.org/dldevinc/sanic-aioja.svg?branch=master)](https://travis-ci.org/dldevinc/sanic-aioja)

## Install
```
pip install sanic-aioja
```

## Features
* Debug mode
* Babel support
* `@jinja2.template` decorator
* Shortcut methods: `globals`, `filters`, `tests`, `extensions` and `policies`
* Built-in `url` and `static` global functions
* Ability to precompile templates

## Example
```python
from sanic import Sanic
from sanic.response import html
from sanic_aioja import Jinja2, FileSystemLoader

app = Sanic("sanic_aioja")

jinja2 = Jinja2(
    app,

    # use DebugUndefined
    debug=True,

    # precompile templates on server start.
    # See jinja2.Environment.compile_templates()
    precompile=True,
    precompile_path=".jinja2.zip",
    
    # Jinja2 options
    trim_blocks=True,
    lstrip_blocks=True,
    loader=FileSystemLoader("./templates"),    
)

# Lets extend environment with some globals
jinja2.globals({
    "token": "extensions.token",
}).policies({
    "ext.i18n.trimmed": True,
})


@app.route('/')
@jinja2.template("index.html")
async def index(request):
    return {
        "header": "Sanic-aioja",
        "array": ["Red", "Green", "Blue"],
    }


@app.route('/render/')
async def index(request):
    content = await jinja2.render_to_string(request, "index.html", {
        "header": "Sanic-aioja",
        "array": ["Red", "Green", "Blue"],
    })
    return html(content)


if __name__ == "__main__":
    app.run()
```
