import graphene
from graphene_django import DjangoObjectType
from .models import Deck



class DeckType(DjangoObjectType):
    class Meta:
        model = Deck

#API for create
class CreateDeck(graphene.Mutation):
    deck = graphene.Field(DeckType)

    class Arguments:
        title = graphene.String()
        description= graphene.String()

    def mutate(self, info, title,description):
        d = Deck(title=title, description=description)
        d.save()
        return CreateDeck(deck=d)

#API for query
class Query(graphene.ObjectType):

    decks = graphene.List(DeckType)
    deck_by_id= graphene.Field(DeckType,deck_id=graphene.ID())

    def resolve_decks(self, info):
        return Deck.objects.all()

    def resolve_deck_by_id(self,info,deck_id):
        return Deck.objects.get(pk=deck_id)


class Mutation(graphene.ObjectType):
    create_deck = CreateDeck.Field()
