from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import StringEntry


class StringAnalyzerAPITest(TestCase):
	def setUp(self):
		self.client = APIClient()

	def test_create_and_get_string(self):
		url = reverse('create-string')
		data = {'value': 'racecar'}
		resp = self.client.post(url, data, format='json')
		self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
		# GET by value
		get_url = reverse('get-string', args=['racecar'])
		get_resp = self.client.get(get_url)
		self.assertEqual(get_resp.status_code, status.HTTP_200_OK)
		self.assertEqual(get_resp.data['value'], 'racecar')

	def test_duplicate_create_returns_409(self):
		url = reverse('create-string')
		data = {'value': 'hello'}
		resp1 = self.client.post(url, data, format='json')
		self.assertEqual(resp1.status_code, status.HTTP_201_CREATED)
		resp2 = self.client.post(url, data, format='json')
		self.assertEqual(resp2.status_code, status.HTTP_409_CONFLICT)

	def test_list_filtering_and_contains_character(self):
		# create some strings
		self.client.post(reverse('create-string'), {'value': 'abc'}, format='json')
		self.client.post(reverse('create-string'), {'value': 'aba'}, format='json')
		# filter by is_palindrome
		resp = self.client.get(reverse('list-strings'), {'is_palindrome': 'true'})
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		self.assertTrue(all(item['properties']['is_palindrome'] for item in resp.data['data']))

	def test_nlp_filter(self):
		self.client.post(reverse('create-string'), {'value': 'level'}, format='json')
		self.client.post(reverse('create-string'), {'value': 'notpal'}, format='json')
		resp = self.client.get(reverse('nlp-filter'), {'query': 'all single word palindromic strings'})
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		self.assertTrue(all(item['properties']['is_palindrome'] for item in resp.data['data']))

	def test_delete_string(self):
		self.client.post(reverse('create-string'), {'value': 'temp'}, format='json')
		del_resp = self.client.delete(reverse('delete-string', args=['temp']))
		self.assertEqual(del_resp.status_code, status.HTTP_204_NO_CONTENT)
		# ensure deleted
		get_resp = self.client.get(reverse('get-string', args=['temp']))
		self.assertEqual(get_resp.status_code, status.HTTP_404_NOT_FOUND)
