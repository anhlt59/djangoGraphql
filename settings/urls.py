from django.contrib import admin
from django.urls import path
from graphene_django.views import GraphQLView
from graphql_jwt.decorators import jwt_cookie


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', jwt_cookie(GraphQLView.as_view(graphiql=True))),
    path('graphql', GraphQLView.as_view(graphiql=True)),
]
