import graphene
import graphql_jwt
from graphene import relay
from graphql_jwt.decorators import login_required
from graphene_django.filter import DjangoFilterConnectionField

from api.models import Movie, Director
from .base import DirectorType, MovieType, MovieNode


class Query(graphene.ObjectType):

    all_movies = graphene.List(MovieType)
    # all_movies = DjangoFilterConnectionField(MovieNode)
    all_directors = graphene.List(DirectorType)
    movie = graphene.Field(MovieType, id=graphene.Int(), title=graphene.String())

    # @login_required
    # def resolve_all_movies(self, info, **kwargs):
    #     # user = info.context.user
    #     # if not user.is_authenticated:
    #     #     raise Exception("Auth credentials were not provided")
    #     return Movie.objects.all()

    def resolve_all_directors(self, info, **kwargs):
        return Director.objects.all()

    def resolve_movie(self, info, **kwargs):
        query_string = ""

        for key, value in kwargs.items():
            if value:
                query_string += f"{key}={value},"

        try:
            movie = eval(f"Movie.objects.get({query_string})")
        except Movie.DoesNotExist:
            movie = None

        return movie
