from unittest.mock import patch
from django.urls import reverse
from recipes.tests.test_recipe_base import RecipeMixin
from rest_framework import test


class RecipeAPIv2TestMixin(RecipeMixin):
    def get_recipe_list_reverse_url(self, reverse_result=None):
        api_url = reverse_result or reverse('recipes:recipes-api-list')
        return api_url

    def get_recipe_api_list(self, reverse_result=None):
        api_url = self.get_recipe_list_reverse_url(reverse_result)
        response = self.client.get(api_url)
        return response

    def get_auth_data(self, username='user', password='pass'):
        userdata = {'username': username, 'password': password}

        user = self.make_author(
            username=userdata.get('username'), password=userdata.get('password')
        )

        response = self.client.post(
            reverse('recipes:token_obtain_pair'), data={**userdata}
        )
        return {
            'jwt_access_token': response.data.get('access'),
            'jwt_refresh_token': response.data.get('refresh'),
            'user': user,
        }

    def get_recipe_raw_data(self):
        return {
            'title': 'This is the title',
            'description': 'This is the description',
            'preparation_time': 1,
            'preparation_time_unit': 'Minutes',
            'servings': '1',
            'servings_unit': 'Person',
            'preparation_steps': 'This is the preparation steps.',
        }


class RecipeAPIv2Test(test.APITestCase, RecipeAPIv2TestMixin):

    def test_recipe_api_list_returns_status_code_200(self):
        response = self.get_recipe_api_list()
        self.assertEqual(response.status_code, 200)

    @patch('recipes.views.api.RecipeAPIv2Pagination.page_size', new=7)
    def test_recipe_api_list_loads_correct_number_of_recipes(self):
        wanted_number_of_recipes = 7
        self.make_recipe_in_batch(qtd=wanted_number_of_recipes)

        response = self.client.get(reverse('recipes:recipes-api-list') + '?page=1')
        qtd_of_loaded_recipes = len(response.data.get('results'))

        self.assertEqual(wanted_number_of_recipes, qtd_of_loaded_recipes)

    def test_recipe_api_do_not_show_not_published_recipes(self):
        recipes = self.make_recipe_in_batch(qtd=2)
        recipe_not_published = recipes[0]
        recipe_not_published.is_published = False
        recipe_not_published.save()

        response = self.get_recipe_api_list()

        self.assertEqual(len(response.data.get('results')), 1)

    @patch('recipes.views.api.RecipeAPIv2Pagination.page_size', new=10)
    def test_recipe_api_lads_recipes_by_category_id(self):
        category_wanted = self.make_category(name='wanted_category')
        category_not_wanted = self.make_category(name='not_wanted_category')

        recipes = self.make_recipe_in_batch(qtd=10)

        for recipe in recipes:
            recipe.category = category_wanted
            recipe.save()

        recipes[0].category = category_not_wanted
        recipes[0].save()

        api_url = (
            reverse('recipes:recipes-api-list') + f'?category_id={category_wanted.id}'
        )
        response = self.get_recipe_api_list(reverse_result=api_url)

        self.assertEqual(len(response.data.get('results')), 9)

    def test_recipe_api_list_user_must_sent_jwt_token_to_create_recipe(self):
        api_url = self.get_recipe_list_reverse_url()
        response = self.client.post(api_url)
        self.assertEqual(response.status_code, 401)

    def test_recipe_api_list_logged_user_can_create_a_recipe(self):
        recipe_raw_data = self.get_recipe_raw_data()
        auth_data = self.get_auth_data()
        jwt_acess_token = auth_data.get('jwt_access_token')
        response = self.client.post(
            self.get_recipe_list_reverse_url(),
            data=recipe_raw_data,
            HTTP_AUTHORIZATION=f'Bearer {jwt_acess_token}',
        )
        self.assertEqual(response.status_code, 201)

    def test_recipe_api_list_logged_user_can_update_a_recipe(self):
        recipe = self.make_recipe()
        auth_data = self.get_auth_data()
        jwt_acess_token = auth_data.get('jwt_access_token')
        author = auth_data.get('user')
        recipe.author = author
        recipe.save()
        new_title = 'New title'

        response = self.client.patch(
            reverse('recipes:recipes-api-detail', args=(recipe.id,)),
            data={'title': new_title},
            HTTP_AUTHORIZATION=f'Bearer {jwt_acess_token}',
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('title'), new_title)

    def test_recipe_api_list_logged_user_cant_update_a_recipe_owned_by_another_user(
        self,
    ):
        recipe = self.make_recipe()
        auth_data = self.get_auth_data(username='Recipe_owner')
        author = auth_data.get('user')
        recipe.author = author
        recipe.save()

        # New user that cant update the recipe
        new_user_auth_data = self.get_auth_data(username='Another_user')
        jwt_acess_token = new_user_auth_data.get('jwt_access_token')

        response = self.client.patch(
            reverse('recipes:recipes-api-detail', args=(recipe.id,)),
            data={},
            HTTP_AUTHORIZATION=f'Bearer {jwt_acess_token}',
        )

        self.assertEqual(response.status_code, 403)
