from django.test import TestCase

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Snack

class SnacksTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user( username="tester", email="tester@email.com", password="123")

        self.snack = Snack.objects.create(title= 'food', description = 'tasty food',purchaser = self.user)

    def test_string_representation(self):
        self.assertEqual(str(self.snack), "food")

    def test_list_page_status(self):
        #Arrange
        url = reverse('snack_list')
        #Act
        response = self.client.get(url)
        #Assert
        self.assertEqual(response.status_code, 200)
        
        

    def test_detail_page_status(self):
        #Arrange
        url = reverse('snack_detail', args='1')
        #Act
        response = self.client.get(url)
        #Assert
        self.assertEqual(response.status_code, 200)

    def test_list_page_templete(self):
        #Arrange
        url = reverse('snack_list')
        #Act
        response = self.client.get(url)
        #Assert
        self.assertTemplateUsed(response, 'snacks/snack_list.html')
        self.assertContains(response, "food")
        self.assertTemplateUsed(response, '_base.html')

    def test_detail_page_templete(self):
        #Arrange
        url = reverse('snack_detail', args='1')
        #Act
        response = self.client.get(url)
        #Assert
        self.assertTemplateUsed(response, 'snacks/snack_detail.html')
        self.assertContains(response, "Snack : food")
        self.assertTemplateUsed(response, '_base.html')
    
    def test_snack_content(self):
        self.assertEqual(f"{self.snack.title}", "food")
        self.assertEqual(f"{self.snack.purchaser}", "tester@email.com")
        self.assertEqual(f'{self.snack.description}', 'tasty food')

    def test_snack_create(self):
        #Arrange
        create_response = self.client.post(
            reverse("snack_create"),
            {
                "title": "Healthy Oat Bar",
                "description": "yummy",
                "purchaser": self.user.id,
            }, follow=True
        )
        
        #Act
        url = reverse('snack_detail', args='2')
        #Assert
        self.assertRedirects(create_response ,url)
        self.assertContains(create_response, "Healthy Oat Bar")

    def test_snack_delete_view(self):
        response = self.client.get(reverse("snack_delete", args="1"))
        self.assertEqual(response.status_code, 200)
    
    def test_snack_update(self):
        #Arrange
        create_response = self.client.post(
            reverse("snack_update", args='1'),
            {
                "title": "Healthy Granula Bar",
                "description": "Extra yummy",
                "purchaser": self.user.id,
            }, follow=True
        )
        
        #Act
        url = reverse('snack_detail', args='1')
        #Assert
        self.assertRedirects(create_response ,url)
        self.assertContains(create_response, "Healthy Granula Bar")
