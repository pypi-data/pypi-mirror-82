from cms import signals
from cms.models import Page
from djangocms_algolia.index import AlgoliaPageDataProxy


def update_page_index(sender, instance: Page, language: str, **kwargs) -> None:
    obj: AlgoliaPageDataProxy = AlgoliaPageDataProxy.objects.get(page=instance, language=language)
    obj.save()


signals.post_publish.connect(update_page_index, Page)
signals.post_unpublish.connect(update_page_index, Page)
