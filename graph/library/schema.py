import graphene
from graphene_django import DjangoObjectType
from .models import *

class AuthorType(DjangoObjectType):
    class Meta:
        model=models.Author

class BookType(DjangoObjectType):
    class Meta:
        model=models.Book

class Query(graphene.ObjectType):
    authors=graphene.List(AuthorType)
    books=graphene.List(BookType)

    books_by_Author=graphene.List(
        BookType,author_family_name=graphene.String(),
    )

    def resolve_authors(self,info):
       return models.Author.objects.all()

    def resolve_books(self,info):
        return models.Book.objects.all()

    def resolve_books_by_author(self,info,author_family_name):
        return models.Book.objects.filter(
            author__family_name=author_family_name,
        ) 

schema=graphene.Schema(query=Query)