from sanic import Sanic
from sanic import response
from jinja2 import Environment, PackageLoader, select_autoescape

import sys

# Enabling async template execution which allows you to take advantage
# of newer Python features requires Python 3.6 or later.
enable_async = sys.version_info >= (3, 6)

app = Sanic(__name__)

# Load the template environment with async support
template_env = Environment(
    loader=PackageLoader('blog_app', 'templates'),
    autoescape=select_autoescape(['html', 'xml']),
    enable_async=enable_async
)

# Load the template from file
template = template_env.get_template("index.html")


@app.route('/')
async def test(request):
    rendered_template = await template.render_async(title='Nice title', posts=[
        {
            "title": "ABC",
            "createdAt": "2018-01-01"
        }, {
            "title": "DEF",
            "createdAt": "2018-01-01"
        }, {
            "title": "GHI",
            "createdAt": "2018-01-01"
        }
    ])
    return response.html(rendered_template)


app.run(host="0.0.0.0", port=8000, debug=True, access_log=False)
