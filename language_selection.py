#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from google.cloud import translate

def translate_text(text, target_language):
    parent = f"projects/projectocr-399718"
    translate_client = translate.TranslationServiceClient()

    response = translate_client.translate_text(
        parent=parent,
        contents=[text],
        target_language_code=target_language,
    )

    translation = response.translations[0].translated_text
    return translation

