from flask import url_for
import urllib.parse


def command_list_routes(app):
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        route = "{:50s} {:20s} {}".format(rule.endpoint, methods, url)
        line = urllib.parse.unquote(route)
        output.append(line)

    for line in sorted(output):
        print(line)
