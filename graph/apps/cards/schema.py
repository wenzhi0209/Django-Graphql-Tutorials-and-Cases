from datetime import timedelta
from django.utils import timezone
import re
import graphene
from graphene_django import DjangoObjectType
from apps.decks.models import Deck
from apps.cards.models import Card
from graphql import GraphQLError

class CardType(DjangoObjectType):
    class Meta:
        model = Card

class Query(graphene.ObjectType):
    cards = graphene.List(CardType)
    
    deck_cards=graphene.List(CardType,deck_id=graphene.ID())

    def resolve_cards(self, info):
        return Card.objects.all()

    def resolve_deck_cards(self,info,deck_id):
        return Card.objects.filter(deck=deck_id)

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

class UpdateCard(graphene.Mutation):
    card=graphene.Field(CardType)

    class Arguments:
        question= graphene.String()
        answer=graphene.String()
        id=graphene.ID()
        # easy,average,or difficult -> 1,2,3
        status=graphene.Int(description="easy,average,or difficult -> 1,2,3")
    
    def mutate(self,info,question,answer,id,status):
        if status not in[1,2,3]:
            raise GraphQLError('Status value out of bounds. It should within 1,2 or 3')

        c =Card.objects.get(pk=id)
        
        re.findall(r'\d+', '')
        
        bucket= c.bucket
        if status ==1 and bucket>1:
            bucket -=1
        elif status ==3 and bucket<5:
            bucket +=1
        
        #calculate next review at date
        days=re.findall(r'\d+', c.buckets[bucket-1][1])[0]
        next_review_at=timezone.now()
        next_review_at= next_review_at + timedelta(days=int(days))

        c.question=question
        c.answer=answer
        c.bucket=bucket
        c.next_review_at=next_review_at
        c.last_review_at=timezone.now()

        c.save()

        return UpdateCard(card=c)


class Mutation(graphene.ObjectType):
    create_card = CreateCard.Field()
    update_card = UpdateCard.Field()


schema = graphene.Schema(query=Query,mutation=Mutation)