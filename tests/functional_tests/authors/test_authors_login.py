import pytest
from .base import AuthorsBaseTest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By


@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):
    def test_user_valid_data_can_login_successfully(self):
        string_password = 'pass'
        user = User.objects.create_user(username='my_user', password=string_password)

        # User opens login page
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # User sees the login form
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')

        # User types its user and password
        username_field.send_keys(user.username)
        password_field.send_keys(string_password)

        # User submits the form
        form.submit()

        # User sees success login message
        self.assertIn(
            f"Your are logged in with {user.username}.",
            self.browser.find_element(By.TAG_NAME, 'body').text,
        )

    def test_login_create_raises_404_if_not_POST_method(self):
        self.browser.get(self.live_server_url + reverse('authors:login_create'))

        self.assertIn('Not Found', self.browser.find_element(By.TAG_NAME, 'body').text)

    def test_form_login_is_invalid(self):
        # User opens login page
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # User sees the form
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        # User tries to login with empty values
        username = self.get_by_placeholder(form, 'Type your username')
        password = self.get_by_placeholder(form, 'Type your password')
        username.send_keys(' ')
        password.send_keys(' ')

        # Submit the form
        form.submit()

        # User sees error message
        self.assertIn(
            'Invalid username or password',
            self.browser.find_element(By.TAG_NAME, 'body').text,
        )

    def test_form_login_invalid_credentials(self):
        # User opens login page
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # User sees the form
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        # User tries to login with wrond credentials
        username = self.get_by_placeholder(form, 'Type your username')
        password = self.get_by_placeholder(form, 'Type your password')
        username.send_keys('invalid_user')
        password.send_keys('invalid_password')

        # Submit the form
        form.submit()

        # User sees error message
        self.assertIn(
            'Invalid credentials',
            self.browser.find_element(By.TAG_NAME, 'body').text,
        )
