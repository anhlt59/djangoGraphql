import graphene
from graphene import relay
from graphene_django.types import DjangoObjectType

from api.models import Movie, Director


class DirectorType(DjangoObjectType):

    class Meta:
        model = Director


class MovieType(DjangoObjectType):

    class Meta:
        model = Movie

    movie_age = graphene.String()

    def resolve_movie_age(self, info):
        return "Old movie" if self.year < 2000 else "New movie"


# just for relay implementation
class MovieNode(DjangoObjectType):

    class Meta:
        model = Movie
        filter_fields = ["title", "year"]
        interfaces = (relay,)