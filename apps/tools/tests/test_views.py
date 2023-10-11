from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient

from apps.accounts.models import CustomUser, Profile
from apps.tools.models import Blog
from cities_light.models import Country, City


class CountryFilterViewTest(APITestCase):
    def test_country_list(self):
        for i in range(15):
            Country.objects.create(name=f'Country {i}')

        url = reverse('country-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('results', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)

        self.assertEqual(len(response.data['results']), 10)


class CityFilterViewTest(APITestCase):
    def setUp(self):
        self.countries = [Country.objects.create(name=f'Country {i}') for i in range(15)]
        self.cities = [City.objects.create(name=f'City {i}', country=self.countries[i]) for i in range(15)]

    def test_city_list(self):
        url = reverse('city-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('results', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)

        self.assertEqual(len(response.data['results']), 10)


class PartnersViewTest(APITestCase):
    def test_partners_list(self):
        url = reverse('partners')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class BlogListViewTest(APITestCase):
    def test_blog_list(self):
        for i in range(15):
            Blog.objects.create(title=f'Blog {i}', body=f'Body {i}')

        url = reverse('blogs-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('results', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)

        self.assertEqual(len(response.data['results']), 10)


class BlogDetailViewTest(APITestCase):
    def setUp(self):
        self.blog = Blog.objects.create(title='Test Blog', body='Test Body')

    def test_blog_detail(self):
        url = reverse('blog-detail', kwargs={'pk': self.blog.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class RatingCreateViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.user_data_1 = {
            'email': 'test1@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'role': 'salon',
        }
        self.user_data_2 = {
            'email': 'test2@example.com',
            'first_name': 'Piter',
            'last_name': 'Parker',
            'role': 'salon',
        }

        self.user1 = CustomUser.objects.create_user(**self.user_data_1)
        self.user2 = CustomUser.objects.create_user(**self.user_data_2)

        self.profile_1 = Profile.objects.get(user=self.user1)
        self.profile_2 = Profile.objects.get(user=self.user2)

        self.url = reverse('rating')

    def test_rating_create(self):
        data = {
            'profile': self.profile_1.user.id,
            'mark': 5,
            'comment': 'Great!'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_rating_create_invalid_data(self):
        data_1 = {
            'profile': 200,
            'mark': 5,
            'comment': 'Good job!'
        }
        data_2 = {
            'profile': self.profile_2.user.id,
            'mark': 0,
            'comment': 'Bad!'
        }

        response = self.client.post(self.url, data_1, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['profile'][0].code, 'does_not_exist')

        response = self.client.post(self.url, data_2, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
