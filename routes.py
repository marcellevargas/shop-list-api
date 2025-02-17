from flask import request, jsonify
from ariadne import make_executable_schema, graphql_sync
from schema.type_defs import type_defs
from schema.resolvers import query, mutation

schema = make_executable_schema(type_defs, query, mutation)

def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(schema, data, context_value=request, debug=True)
    status_code = 200 if success else 400
    return jsonify(result), status_code

def graphql_playground():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8" />
        <title>GraphQL Playground</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/graphql-playground/1.7.33/static/css/index.css" />
        <script src="https://cdnjs.cloudflare.com/ajax/libs/graphql-playground/1.7.33/static/js/middleware.js"></script>
    </head>
    <body>
        <div id="root"></div>
        <script>
            window.addEventListener("load", function () {
                GraphQLPlayground.init(document.getElementById("root"), {
                    endpoint: "/graphql"
                })
            })
        </script>
    </body>
    </html>
    """, 200
