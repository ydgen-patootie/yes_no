from unittest import mock
from unittest.mock import patch, PropertyMock

from rest_framework import status
from rest_framework.test import APITestCase
from mixer.backend.django import mixer
from django.contrib.auth import get_user_model

from core.models import Question, Answer
from core.services import AnswerFromYesno


class TestUserFixture(APITestCase):

    password = 'pass'

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = mixer.blend(User)
        cls.user.set_password(cls.password)
        cls.user.save()


class TestQuestionFixture(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.question = mixer.blend(Question)


class TestToken(TestUserFixture):

    def test_register(self):

        username = 'user1'
        password = 'pass1234567!'

        url = '/register/'

        data = {'username': username,
                'password': password,
                'password2': password,
                }

        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_login(self):

        url = '/login/'

        data = {'username': self.user.username,
                'password': self.password,
                }

        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in resp.data)

    def test_question_not_logged(self):

        url = '/question/'

        data = {'question_text': 'pass',
                }

        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class TestAnswerFromYesno(TestQuestionFixture):

    def test_empty_answer(self):

        instance = AnswerFromYesno(self.question)
        instance.save_answer()

        ans = Answer.objects.get(id=1)
        self.assertEqual(ans.question, self.question)
        self.assertIsNone(ans.answer_text)
        self.assertIsNone(ans.image_url)

    @mock.patch('core.services.requests.get')
    def test_filled_answer(self, mock_get):

        answer = 'no'
        image = 'https://123.gif'
        mock_data = {'answer': answer,
                     'forced': False,
                     'image': image}

        mock_response = mock.Mock()
        mock_response.json.return_value = mock_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        instance = AnswerFromYesno(self.question)
        instance.get_answer()
        instance.save_answer()
        ans = Answer.objects.get(id=1)
        self.assertEqual(ans.question, self.question)
        self.assertEqual(ans.answer_text, answer)
        self.assertEqual(ans.image_url, image)

    def test_filled_answer_no_connection(self):

        with patch.object(AnswerFromYesno, 'url_to_yesno', new_callable=PropertyMock) as attr_mock:
            attr_mock.return_value = 'a.com'

            instance = AnswerFromYesno(self.question)
            instance.get_answer()
            instance.save_answer()

        ans = Answer.objects.get(id=1)
        self.assertEqual(ans.question, self.question)
        self.assertIsNone(ans.answer_text)
        self.assertIsNone(ans.image_url)


class TestQuestionView(TestUserFixture):

    @mock.patch('core.services.requests.get')
    def test_from_register_to_question(self, mock_get):

        answer = 'yes'
        question_text = 'test!'
        image = 'https://123.gif'
        mock_data = {'answer': answer,
                     'forced': False,
                     'image': image}

        mock_response = mock.Mock()
        mock_response.json.return_value = mock_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        url = '/login/'

        data = {'username': self.user.username,
                'password': self.password,
                }

        resp = self.client.post(url, data, format='json')
        token = resp.data['access']

        url = '/question/'

        data = {'question_text': question_text,
                }

        resp = self.client.post(url, data, HTTP_AUTHORIZATION=f'Bearer {token}', format='json')
        self.assertEqual(resp.data['answer'], answer)
        ans = Answer.objects.get(id=1)
        que = Question.objects.get(id=1)
        self.assertEqual(que.user, self.user)
        self.assertEqual(que.question_text, question_text)
        self.assertEqual(ans.answer_text, answer)
        self.assertEqual(ans.image_url, image)
        self.assertEqual(ans.question, que)


