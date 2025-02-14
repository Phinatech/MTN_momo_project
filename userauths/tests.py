# from django.test import TestCase, Client
# from django.urls import reverse
# from django.contrib.auth import get_user_model
# from userauths.models import Profile

# User = get_user_model()

# class UserAuthTests(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_user(
#             username='testuser', email='testuser@example.com', password='TestPassword123'
#         )

#     def test_register_view_get(self):
#         response = self.client.get(reverse('userauths:sign-up'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'userauths/sign-up.html')

#     def test_register_view_post(self):
#         response = self.client.post(reverse('userauths:sign-up'), {
#             'username': 'newuser',
#             'email': 'newuser@example.com',
#             'first_name': 'New',
#             'last_name': 'User',
#             'password1': 'StrongPass123',
#             'password2': 'StrongPass123'
#         })
#         self.assertEqual(response.status_code, 302)  # Redirect after registration
#         self.assertTrue(User.objects.filter(username='newuser').exists())

#     def test_login_view_get(self):
#         response = self.client.get(reverse('userauths:sign-in'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'userauths/sign-in.html')

#     def test_login_view_post(self):
#         response = self.client.post(reverse('userauths:sign-in'), {
#             'email': 'testuser@example.com',
#             'password': 'TestPassword123'
#         })
#         self.assertEqual(response.status_code, 302)  # Redirect after login
#         self.assertTrue('_auth_user_id' in self.client.session)

#     def test_logout_view(self):
#         self.client.login(email='testuser@example.com', password='TestPassword123')
#         response = self.client.get(reverse('userauths:sign-out'))
#         self.assertEqual(response.status_code, 302)  # Redirect after logout
#         self.assertFalse('_auth_user_id' in self.client.session)

#     def test_my_profile_view(self):
#         self.client.login(email='testuser@example.com', password='TestPassword123')
#         response = self.client.get(reverse('userauths:my_profile'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'userauths/profile.html')

#     def test_settings_view(self):
#         self.client.login(email='testuser@example.com', password='TestPassword123')
#         response = self.client.get(reverse('userauths:settings'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'userauths/settings.html')

#     def test_change_password_view(self):
#         self.client.login(email='testuser@example.com', password='TestPassword123')
#         response = self.client.post(reverse('userauths:change_password'), {
#             'old_password': 'TestPassword123',
#             'new_password1': 'NewTestPass123',
#             'new_password2': 'NewTestPass123'
#         })
#         self.assertEqual(response.status_code, 302)
#         self.user.refresh_from_db()
#         self.assertTrue(self.user.check_password('NewTestPass123'))

#     def test_delete_account_view(self):
#         self.client.login(email='testuser@example.com', password='TestPassword123')
#         response = self.client.post(reverse('userauths:delete_account'), {
#             'confirm_delete': 'on'
#         })
#         self.assertEqual(response.status_code, 302)
#         self.assertFalse(User.objects.filter(username='testuser').exists())
