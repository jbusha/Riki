import unittest
import os
from wiki import create_app
from wiki.web import current_users

'''
ADD A 1 TO THE USERNAME IN LINE 40 WHENEVER YOU RUN THIS TEST
Not sure why the delete_users method works for all other tests except this one
'''
class UserSignUpTestCases(unittest.TestCase):
    def setUp(self):
        path = os.getcwd()
        self.app = create_app(directory=path)
        self.app.config['WTF_CSRF_ENABLED'] = False  # no CSRF during tests
        self.client = self.app.test_client()

    def delete_user_name(self, app):
        with app.app_context():
            current_users.delete_user("test_user")

    def test_home_page_redirect(self):
        response = self.client.get('/', follow_redirects=True)
        assert response.status_code == 200
        # assert response.request.path == '/user/signup'

    def test_signup_page_visible(self):
        response = self.client.get('/user/signup/')
        assert response.status_code == 200
        html = response.get_data(as_text=True)

        # make sure all the fields are included
        assert 'id="username"' in html
        assert 'id="password"' in html
        assert 'id="confirm_pass"' in html
        assert 'value="Sign Up"' in html

    def test_register_user_success(self):
        # register a new user
        response = self.client.post('/user/signup/', data={
            'username': 'test_user1',
            'password': 'TestPass12',
            'confirm_pass': 'TestPass12',
        }, follow_redirects=True)
        html = response.get_data(as_text=True)
        print(html)
        assert response.status_code == 200
        assert 'Sign up successful.' in html

    def test_register_user_duplicate(self):
        # test a username that is already in the database
        response = self.client.post('/user/signup/', data={
            'username': 'user',
            'password': 'TestPass12',
            'confirm_pass': 'TestPass12',
        }, follow_redirects=True)
        html = response.get_data(as_text=True)
        assert response.status_code == 200
        assert 'Username has already been taken.' in html

    def test_register_user_password_mismatch(self):
        # test the instance of passwords not matching
        response = self.client.post('/user/signup/', data={
            'username': 'test_user', # change for each test ran
            'password': 'TestPass12',
            'confirm_pass': 'TestPass',
        }, follow_redirects=True)
        html = response.get_data(as_text=True)
        assert response.status_code == 200
        assert 'Passwords must match.' in html

    def test_register_user_password_no_int(self):
        # test the instance of passwords not meeting the requirements (not having a number)
        response = self.client.post('/user/signup/', data={
            'username': 'test_user',
            'password': 'TestPass',
            'confirm_pass': 'TestPass',
        }, follow_redirects=True)
        html = response.get_data(as_text=True)
        assert response.status_code == 200
        assert 'Password must contain at least one digit.' in html

    def test_register_user_password_short(self):
        # test the instance of passwords not meeting the requirements (less than 6 characters)
        response = self.client.post('/user/signup/', data={
            'username': 'test_user',
            'password': 'Test1',
            'confirm_pass': 'Test1',
        }, follow_redirects=True)
        html = response.get_data(as_text=True)
        assert response.status_code == 200
        assert 'Password must be at least 6 characters long.' in html

if __name__ == '__main__':
    unittest.main()
