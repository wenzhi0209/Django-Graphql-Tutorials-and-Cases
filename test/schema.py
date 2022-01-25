from datetime import datetime
import imp
import graphene
import json
from datetime import datetime

class User(graphene.ObjectType):
    id=graphene.ID()
    username=graphene.String()
    last_login=graphene.DateTime(required=False)



class Query(graphene.ObjectType):
    users=graphene.List(User,first=graphene.Int())
    
    def resolve_users(self,info,first):
        return [
            User(username='Alice',last_login=datetime.now()),
            User(username='Bright',last_login=datetime.now()),
            User(username='Steve',last_login=datetime.now()),
            User(username='Allian',last_login=datetime.now()),
        ][:first]


    is_staff=graphene.Boolean()

    def resolve_is_staff(self,info):
        return True

class CreateUser(graphene.Mutation):
    class Arguments:
        username=graphene.String()
    
    user=graphene.Field(User)

    def mutate(self,info,username):
        if info.context.get('is_vip'):
            username=username.upper()
        user=User(username=username)
        return CreateUser(user=user)



class Mutations(graphene.ObjectType):
    create_user=CreateUser.Field()

schema=graphene.Schema(query=Query, mutation=Mutations)

result=schema.execute(
    '''
    mutation createUser($username:String){
        createUser(username:$username){
            user{
                username
            }
        }
    }
    
    ''',
    variable_values={'username':'tester3'},
    context={'is_vip':True}
)
items =dict(result.data.items())
print(json.dumps(items,indent=4))