import os

current_languages = [
    "pt_BR",  # Portuques (Brazil)
    "en_US",  # English (United States)
    "ru_RU",  # Russian (Russia)
    "es_ES",  # Spanish (Spain)
    "fr_FR",  # French (France)
    "de_DE",  # German (Germany)
    "ja_JP",  # Japanese (Japan)
    "zh_CN"  # Mandarin (Simplified, China)
]


def load_lang(self, language='pt_BR'):
  if language in current_languages:
    try:
      with open(f'locales/{language}.locale') as f:
        data = f.read().splitlines()
        return data
    except:
      with open(f'locales/pt_BR.locale') as f:
        data = f.read().splitlines()
        return data
  else:
    with open(f'locales/pt_BR.locale') as f:
      data = f.read().splitlines()
      return data
