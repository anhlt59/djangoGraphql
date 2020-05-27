import graphene
from graphene import relay
import graphql_jwt
from api.models import Movie, Director

from .base import DirectorType, MovieType


class MovieCreateMutation(graphene.Mutation):

    class Arguments:
        title = graphene.String(required=True)
        year = graphene.Int(required=True)

    movie = graphene.Field(MovieType)

    def mutate(self, info, **kwargs):
        """two way to pass arguments
        1. title, year,...
        2. **kwargs
        """
        if (title := kwargs.get("title", None)) and (year := kwargs.get("year", None)):
            movie = Movie.objects.create(title=title, year=year)
            mutation = MovieCreateMutation(movie=movie)
        else:
            mutation = None

        return mutation


class MovieUpdateMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        year = graphene.Int()
        id = graphene.ID(required=True)

    movie = graphene.Field(MovieType)

    def mutate(self, info, **kwargs):
        if id := kwargs.get('id', None):
            movie = Movie.objects.get(pk=id)

            if title := kwargs.get('title', None):
                movie.title = title
            if year := kwargs.get('year', None):
                movie.year = year
            if director := kwargs.get('director', None):
                movie.director = director
            movie.save()
        else:
            movie = None

        return MovieUpdateMutation(movie=movie)


class MovieDeleteMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    movie = graphene.Field(MovieType)

    def mutate(self, info, **kwargs):
        if id := kwargs.get('id', None):
            try:
                Movie.objects.get(pk=id).delete()
            except Movie.DoesNotExist:
                pass

        return MovieDeleteMutation(movie=None)


class Mutation:
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    # verify_token = graphql_jwt.Verify.Field()
    # refresh_token = graphql_jwt.Refresh.Field()
    # revoke_token = graphql_jwt.Revoke.Field()

    create_movie = MovieCreateMutation.Field()
    update_movie = MovieUpdateMutation.Field()
    delete_movie = MovieDeleteMutation.Field()