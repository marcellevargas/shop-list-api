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
