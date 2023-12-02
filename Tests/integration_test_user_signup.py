# John Busha

import unittest
import os
from flask import Flask
from wiki import create_app
from wiki.web import current_users

class TestUserSignupIntegration(unittest.TestCase):
    def setUp(self):
        path = os.getcwd()
        self.app = create_app(directory=path)
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()

        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_signup_form_integration(self):
        response = self.client.get('/user/signup', follow_redirects=True)
        self.assertIn(response.status_code, [200, 302, 308])
        html = response.get_data(as_text=True)

        self.assertIn('Username', html)
        self.assertIn('Password', html)
        self.assertIn('Confirm Password', html)
        self.assertIn('Show/Hide Password', html)
        self.assertIn('Sign Up', html)

        self.assertIn('<form', html)
        self.assertIn('method="POST"', html)

        self.assertIn('Already have a profile?', html)
        self.assertIn('href="/user/login/"', html)

        submit = self.client.post('/user/signup/', data={'username': 'user', 'password': '123456', 'confirm_pass': '123456', }, follow_redirects=True)
        self.assertIn(submit.status_code, [200, 302, 308])
        submit_html = submit.get_data(as_text=True)
        
        self.assertIn('Username has already been taken.', submit_html)

    def test_login_form_integration(self):
        response = self.client.get('/user/login', follow_redirects=True)
        self.assertIn(response.status_code, [200, 302, 308])
        html = response.get_data(as_text=True)

        self.assertIn('Username', html)
        self.assertIn('Password', html)
        self.assertIn('Login', html)

        self.assertIn('<form', html)
        self.assertIn('method="POST"', html)

        self.assertIn('Don\'t have a profile?', html)
        self.assertIn('href="/user/signup/"', html)

        submit = self.client.post('/user/login/', data={'username': 'user', 'password': '123456', }, follow_redirects=True)
        self.assertIn(submit.status_code, [200, 302, 308])
        submit_html = submit.get_data(as_text=True)

        self.assertIn('Errors occured verifying your input.', submit_html)

if __name__ == '__main__':
    unittest.main()