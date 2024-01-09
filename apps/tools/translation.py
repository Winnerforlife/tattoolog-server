from modeltranslation.translator import register, TranslationOptions
from apps.tools.models import Festival


@register(Festival)
class FestivalTranslationOptions(TranslationOptions):
    fields = ('about', 'rules')
