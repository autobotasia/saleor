import graphene

from graphene_federation import key
from ...social import models
from ..core.connection import CountableDjangoObjectType
from ..store.types import Store
from ..account.types import User
from ..meta.types import ObjectWithMetadata


class Social(CountableDjangoObjectType):
    follow = graphene.Boolean(
        description="follow action.",
        required=True,
    )
    store = graphene.Field(
        Store,
        id=graphene.Argument(graphene.ID, description="ID of the store."),
        description="Look up a store type by ID",
    )
    user = graphene.Field(
        User,
        id=graphene.Argument(graphene.ID, description="ID of the user."),
        description="Look up a user type by ID",
    )    

    class Meta:
        description = (
            "social follow action."
        )
        only_fields = [
            "follow",
            "user",
            "store"
        ]
        model = models.Social
        interfaces = [graphene.relay.Node, ObjectWithMetadata]
