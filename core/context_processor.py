from django.conf import settings

def postage_settings(request):
    return{
        'small_first_class':settings.SMALL_FIRST_CLASS,
        'small_second_class':settings.SMALL_SECOND_CLASS,
        'large_first_class':settings.LARGE_FIRST_CLASS,
        'large_second_class':settings.LARGE_SECOND_CLASS,
    }