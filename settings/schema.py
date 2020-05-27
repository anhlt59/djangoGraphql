import graphene
from api.schema import (
    query as api_query,
    mutation as api_mutation
)


class Query(api_query.Query, graphene.ObjectType):
    pass


class Mutation(api_mutation.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(
    query=Query,
    mutation=Mutation
)