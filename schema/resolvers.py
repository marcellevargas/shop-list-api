from ariadne import QueryType, MutationType
from models.models import db, Product

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
