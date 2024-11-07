from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habits
from users.models import User


class HabitsTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="django@mail.ru", password='DXB')
        self.habit = Habits.objects.create(
            owner=self.user, place="Home", time="12:00:00", action="Зарядка", duration='40'
        )
        self.client.force_authenticate(user=self.user)

    def test_habits_retrieve(self):
        url = reverse("habits:habits_retrieve", args=(self.habit.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("place"), self.habit.place)

    def test_habits_create(self):
        url = reverse("habits:habits_create")
        data = {
            "owner": self.user.pk,
            "place": "Home",
            "time": "12:00",
            "action": "Зарядка",
            "duration": "40",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habits.objects.all().count(), 2)

    def test_habits_update(self):
        url = reverse("habits:habits_update", args=(self.habit.pk,))
        data = {
            "place": "Work",
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Habits.objects.get(pk=self.habit.pk).place, "Work")

    def test_habits_delete(self):
        url = reverse("habits:habits_delete", args=(self.habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habits.objects.all().count(), 0)

    def test_habits_list(self):
        url = reverse(
            "habits:habits_list",
        )
        response = self.client.get(url)
        data = response.status_code
        print(data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
