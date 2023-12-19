# from inspect import signature
from recipes.tests.test_recipe_base import RecipeTestBase
from django.core.files import File

from random import randint
from faker import Faker
import requests


def rand_ratio():
    return randint(840, 900), randint(473, 573)


fake = Faker('pt_BR')
# print(signature(fake.random_number))


def make_recipe():
    return {
        'id': fake.random_number(digits=2, fix_len=True),
        'title': fake.sentence(nb_words=6),
        'description': fake.sentence(nb_words=12),
        'preparation_time': fake.random_number(digits=2, fix_len=True),
        'preparation_time_unit': 'Minutos',
        'servings': fake.random_number(digits=2, fix_len=True),
        'servings_unit': 'Porção',
        'preparation_steps': fake.text(3000),
        'created_at': fake.date_time(),
        'author': {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
        },
        'category': {
            'name': fake.word()
        },
        'cover': {
            'url': 'https://loremflickr.com/%s/%s/food,cook' % rand_ratio(),
        }
    }

def make_saved_recipe():
    recipe_original_dict = make_recipe()
    author_original_dict = recipe_original_dict.get('author', {})
    category_original_dict = recipe_original_dict.get('category', {})
    recipe_dict = {
        'title': recipe_original_dict.get('title', ''),
        'description': recipe_original_dict.get('description', ''),
        'preparation_time': recipe_original_dict.get('preparation_time', 0),
        'preparation_time_unit': recipe_original_dict.get('preparation_time_unit', ''),
        'servings': recipe_original_dict.get('servings', ''),
        'servings_unit': recipe_original_dict.get('servings_unit', ''),
        'preparation_steps': recipe_original_dict.get('preparation_steps', ''),
        'slug': f"{recipe_original_dict.get('title', '').replace(' ', '-').replace('.', '')}-{str(rand_ratio()[0])}",
        'author_data': {
            'first_name': author_original_dict.get('first_name', ''),
            'last_name': author_original_dict.get('last_name', ''),
            'username': f"{author_original_dict.get('first_name', '')}_{author_original_dict.get('last_name', '')}"
        },
        'category_data': {
            'name': category_original_dict.get('name', '')
        }
    }
    recipe_test_object = RecipeTestBase()
    recipe = recipe_test_object.make_recipe(**recipe_dict)

    img_url = recipe_original_dict.get("cover", {}).get("url")
    if img_url is not None:
        img_data = requests.get(img_url).content
        img_name = f'{recipe.slug}.jpg'
        img_full_path = f'./utils/recipes/tmp/{img_name}'
        with open(img_full_path, 'wb') as handler:
            handler.write(img_data)
        recipe.cover.save(img_name, File(open(img_full_path, 'rb')))

    return recipe

if __name__ == '__main__':
    from pprint import pprint
    pprint(make_recipe())
