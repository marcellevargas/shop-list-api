from flask import Flask, request, jsonify
from ariadne import QueryType, MutationType, make_executable_schema, graphql_sync

from models.models import db, Product

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shoplist.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Inicializar o SQLAlchemy com o Flask

# Definir o schema GraphQL
type_defs = """
    type Product {
        id: ID!
        title: String!
        purchased: Boolean!
    }

    type Query {
        products: [Product!]!
        product(id: ID!): Product
    }

    input ProductInput {
        title: String!
        purchased: Boolean
    }

    type Mutation {
        createProduct(input: ProductInput!): Product!
        updateProduct(id: ID!, input: ProductInput!): Product!
        deleteProduct(id: ID!): Boolean!
    }
"""

# Queries
query = QueryType()

@query.field("products")
def resolve_products(*_):
    return Product.query.all()

@query.field("product")
def resolve_product(_, info, id):
    return Product.query.get(id)

# Mutations
mutation = MutationType()

@mutation.field("createProduct")
def resolve_create_product(_, info, input):
    new_product = Product(title=input["title"], purchased=input.get("purchased", False))
    db.session.add(new_product)
    db.session.commit()
    return new_product

@mutation.field("updateProduct")
def resolve_update_product(_, info, id, input):
    product = Product.query.get(id)
    if not product:
        raise Exception("Product not found")
    product.title = input.get("title", product.title)
    product.purchased = input.get("purchased", product.purchased)
    db.session.commit()
    return product

@mutation.field("deleteProduct")
def resolve_delete_product(_, info, id):
    product = Product.query.get(id)
    if not product:
        raise Exception("Product not found")
    db.session.delete(product)
    db.session.commit()
    return True

# Criar o schema executável
schema = make_executable_schema(type_defs, query, mutation)

# Endpoint GraphQL Playground
@app.route("/graphql", methods=["GET"])
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

# Endpoint GraphQL para POST requests
@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(schema, data, context_value=request, debug=True)
    status_code = 200 if success else 400
    return jsonify(result), status_code

# Criar o banco de dados se não existir
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Criar tabelas no banco de dados
    app.run(debug=True)