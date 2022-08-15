from modeltranslation.translator import translator, TranslationOptions
from .models import Category, Product


class CategoryTranslationOptions(TranslationOptions):
    fields = ('title',)


class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'warranty', 'return_policy')


translator.register(Category, CategoryTranslationOptions)
translator.register(Product, ProductTranslationOptions)
