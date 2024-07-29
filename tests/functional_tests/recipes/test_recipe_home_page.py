from unittest.mock import patch
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import RecipeBaseFunctionalTest


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipes found here 🥲', body.text)

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_search_input_can_find_correct_recipes(self):
        recipes = self.make_recipe_in_batch()
        search_title = recipes[0].title

        # Abre a página
        self.browser.get(self.live_server_url)

        # Pega o input de busca na página
        search_input = self.browser.find_element(
            By.XPATH, '//input[@placeholder="Search for a recipe"]'
        )

        # Clica no input e digita o termo de busca para encontrar a receita
        search_input.send_keys(search_title)
        search_input.send_keys(Keys.ENTER)

        # Verifica se a receita buscada aparece na tela
        self.assertIn(
            search_title,
            self.browser.find_element(By.CLASS_NAME, 'main-content-list').text,
        )
