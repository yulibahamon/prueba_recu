import graphene
import ventas.schema

class Query(ventas.schema.Query, graphene.ObjectType):
    """Query root para la API GraphQL"""
    pass

schema = graphene.Schema(query=Query)