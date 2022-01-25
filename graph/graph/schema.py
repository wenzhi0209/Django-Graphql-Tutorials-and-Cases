from black import nullcontext
import graphene
from graphene_django import DjangoObjectType
from apps.users.models import User
from apps.decks.models import Deck
from apps.cards.models import Card

# class Query(graphene.ObjectType):
class UserType(DjangoObjectType):
    class Meta:
        model = User


class DeckType(DjangoObjectType):
    class Meta:
        model = Deck


class CardType(DjangoObjectType):
    class Meta:
        model = Card


class Query(graphene.ObjectType):
    users = graphene.List(UserType)

    decks = graphene.List(DeckType)
    deck_by_id= graphene.Field(DeckType,deck_id=graphene.ID())

    cards = graphene.List(CardType)
    
    deck_cards=graphene.List(CardType,deck_id=graphene.ID())

    def resolve_users(self, info):
        return User.objects.all()

    def resolve_decks(self, info):
        return Deck.objects.all()

    def resolve_deck_by_id(self,info,deck_id):
        return Deck.objects.get(pk=deck_id)

    def resolve_cards(self, info):
        return Card.objects.all()

    def resolve_deck_cards(self,info,deck_id):
        return Card.objects.filter(deck=deck_id)


class CreateDeck(graphene.Mutation):
    deck = graphene.Field(DeckType)

    class Arguments:
        title = graphene.String()
        description= graphene.String()

    def mutate(self, info, title,description):
        d = Deck(title=title, description=description)
        d.save()
        return CreateDeck(deck=d)


class CreateCard(graphene.Mutation):
    card = graphene.Field(CardType)

    class Arguments:
        question = graphene.String()
        answer = graphene.String()
        deck_id =graphene.ID()

    def mutate(self, info, question, answer,deck_id):
        d = Deck.objects.get(id=deck_id)
        c = Card(question=question, answer=answer,deck=d)
        c.save()
        return CreateCard(card=c)

class Mutation(graphene.ObjectType):
    create_card = CreateCard.Field()
    create_deck = CreateDeck.Field()

schema = graphene.Schema(query=Query,mutation=Mutation)
