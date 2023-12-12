from django.urls import reverse, resolve
from recipes.tests.test_recipe_base import RecipeTestBase

from recipes import views as recipes_views

class RecipeViewsTest(RecipeTestBase):
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, recipes_views.home)

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, recipes_views.recipe)

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'id': 1}))
        self.assertIs(view.func, recipes_views.category)

    def test_recipe_home_view_returns_status_code_200_ok(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn('No recipes found', response.content.decode('utf-8'))

    def test_recipe_home_view_loads_recipes(self):
        recipe = self.make_recipe()
        response = self.client.get(reverse('recipes:home'))
        context = response.context['recipes']
        self.assertEqual(len(context), 1)
        self.assertIn(recipe, context)

    def test_recipe_detail_returns_404_if_no_recipes(self):
        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 100000}))
        self.assertEqual(response.status_code, 404)
