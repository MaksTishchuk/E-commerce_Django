from django.http import HttpResponseRedirect
from django.utils import translation


def select_language(request):
    if request.method == 'POST':
        cur_language = translation.get_language()
        last_url = request.META.get('HTTP_REFERER')
        final_string = '/'.join(last_url.split('/')[4:])
        lang = request.POST['language']
        translation.activate(lang)
        request.session[translation.LANGUAGE_SESSION_KEY] = lang
        return HttpResponseRedirect("/"+lang+"/"+final_string)
