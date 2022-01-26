
import graphene

from apps.decks.schema import Query as DeckQuery
from apps.decks.schema import Mutation as DeckMutation

from apps.cards.schema import Query as CardQuery
from apps.cards.schema import Mutation as CardMutation

from apps.users.schema import Query as UserQuery
#from apps.users.schema import Mutation as UserMutation


class Query(DeckQuery,CardQuery,UserQuery,graphene.ObjectType):
    pass


class Mutation(DeckMutation,CardMutation,graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query,mutation=Mutation)
