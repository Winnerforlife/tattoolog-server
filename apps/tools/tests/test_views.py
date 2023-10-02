from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase
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
