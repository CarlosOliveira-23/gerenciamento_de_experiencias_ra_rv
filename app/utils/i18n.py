import gettext
from fastapi import Request


SUPPORTED_LANGUAGES = ["en", "pt", "es", "fr"]
DEFAULT_LANGUAGE = "en"


def get_locale_from_request(request: Request) -> str:
    """ Obtém o idioma do cabeçalho 'Accept-Language' da requisição """
    accept_language = request.headers.get("Accept-Language", DEFAULT_LANGUAGE)
    lang_code = accept_language.split(",")[0].strip().lower()

    if lang_code in SUPPORTED_LANGUAGES:
        return lang_code
    return DEFAULT_LANGUAGE


def translate(message: str, lang: str) -> str:
    """ Traduz a mensagem para o idioma especificado """
    locale_dir = "app/locales"
    translator = gettext.translation("messages", localedir=locale_dir, languages=[lang], fallback=True)
    translator.install()
    return translator.gettext(message)
