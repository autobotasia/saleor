import graphene
from graphene_federation import key

from ...attribute import models as attribute_models
from ...core.permissions import PagePermissions
from ...page import models
from ..attribute.filters import AttributeFilterInput
from ..attribute.types import Attribute, SelectedAttribute
from ..core.connection import CountableDjangoObjectType
from ..core.fields import FilterInputConnectionField
from ..decorators import permission_required
from ..meta.types import ObjectWithMetadata
from ..translations.fields import TranslationField
from ..translations.types import PageTranslation
from .dataloaders import (
    PageAttributesByPageTypeIdLoader,
    PagesByPageTypeIdLoader,
    PageTypeByIdLoader,
    SelectedAttributesByPageIdLoader,
)
from ..store.types import Store

@key(fields="id")
class PageMedia(CountableDjangoObjectType):
    is_active = graphene.Boolean(
        required=False, description="Delete image for page."
    )
    class Meta:
        description = "Represents a page media."
        fields = ["alt", "id", "image", "sort_order", "type", "is_active"]
        interfaces = [graphene.relay.Node]
        model = models.PageMedia

    @staticmethod
    def __resolve_reference(root, _info, **_kwargs):
        return graphene.Node.get_node_from_global_id(_info, root.id)

class Page(CountableDjangoObjectType):
    content_json = graphene.JSONString(
        description="Content of the page (JSON).",
        deprecation_reason=(
            "Will be removed in Saleor 4.0. Use the `content` field instead."
        ),
        required=True,
    )
    translation = TranslationField(PageTranslation, type_name="page")
    attributes = graphene.List(
        graphene.NonNull(SelectedAttribute),
        required=True,
        description="List of attributes assigned to this product.",
    )
    media = graphene.List(
        graphene.NonNull(lambda: PageMedia),
        description="List of media for the page.",
    )
    store = graphene.Field(
        Store,
        id=graphene.Argument(graphene.ID, description="ID of the store."),
        slug=graphene.Argument(graphene.String, description="Slug of the store"),
        description="Look up a store by ID or slug.",
    )

    class Meta:
        description = (
            "A static page that can be manually added by a shop operator through the "
            "dashboard."
        )
        only_fields = [
            "content",
            "created",
            "id",
            "is_published",
            "page_type",
            "publication_date",
            "seo_description",
            "seo_title",
            "slug",
            "title",
            "store",
        ]
        interfaces = [graphene.relay.Node, ObjectWithMetadata]
        model = models.Page

    @staticmethod
    def resolve_page_type(root: models.Page, info):
        return PageTypeByIdLoader(info.context).load(root.page_type_id)

    @staticmethod
    def resolve_content_json(root: models.Page, info):
        content = root.content
        return content if content is not None else {}

    @staticmethod
    def resolve_attributes(root: models.Page, info):
        return SelectedAttributesByPageIdLoader(info.context).load(root.id)

    @staticmethod
    def resolve_media(self, info, page=None, slug=None, channel=None, **_kwargs):
        return models.PageMedia.objects.filter(page_id=self.pk, is_active=True)


@key(fields="id")
class PageType(CountableDjangoObjectType):
    attributes = graphene.List(
        Attribute, description="Page attributes of that page type."
    )
    available_attributes = FilterInputConnectionField(
        Attribute,
        filter=AttributeFilterInput(),
        description="Attributes that can be assigned to the page type.",
    )
    has_pages = graphene.Boolean(description="Whether page type has pages assigned.")

    class Meta:
        description = (
            "Represents a type of page. It defines what attributes are available to "
            "pages of this type."
        )
        interfaces = [graphene.relay.Node, ObjectWithMetadata]
        model = models.PageType
        only_fields = ["id", "name", "slug"]

    @staticmethod
    def resolve_attributes(root: models.PageType, info):
        return PageAttributesByPageTypeIdLoader(info.context).load(root.pk)

    @staticmethod
    @permission_required(PagePermissions.MANAGE_PAGES)
    def resolve_available_attributes(root: models.PageType, info, **kwargs):
        return attribute_models.Attribute.objects.get_unassigned_page_type_attributes(
            root.pk
        )

    @staticmethod
    @permission_required(PagePermissions.MANAGE_PAGES)
    def resolve_has_pages(root: models.PageType, info, **kwargs):
        return (
            PagesByPageTypeIdLoader(info.context)
            .load(root.pk)
            .then(lambda pages: bool(pages))
        )
