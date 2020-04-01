from django.test import TestCase, Client
from .models import User, Post, Group
from django.urls import reverse


class UsersExpirenceWorkWithPostTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(first_name='Obi-Wan',
                                             last_name='Kenobi',
                                             username='ben',
                                             email='ben.kenobi@jedi.korusant',
                                             password='OnlyASithDealsInAbsolutes')
        self.post = Post.objects.create(
            text="Who is more stupid: the fool or the fool, who follows him?",
            author=self.user, )

    def test_profile(self):
        response = self.client.get(f'/{self.user.username}/')
        self.assertEqual(response.status_code, 200, msg="Не удается получить профиль пользователя")

    def test_user_create_post(self):
        c = self.client
        login = c.post('/auth/login/', {'username': 'ben', 'password': 'OnlyASithDealsInAbsolutes'})
        self.assertEqual(login.status_code, 302, msg="Не удается войти в учетную запись")
        c.post('/new/', {'text': 'test text', })
        post = Post.objects.filter(text__contains='test text')
        self.assertTrue(post, msg="Пост не опубликован")

    def test_redirect_not_authorized_user(self):
        response = self.client.get("/new/")
        self.assertRedirects(response, '/auth/login/?next=%2Fnew%2F',
                             status_code=302,
                             target_status_code=200,
                             msg_prefix='неавторизованный пользователь не пренаправлен на страницу авторизации',)

    def test_contain_post_in_index_profile_post(self):
        c = self.client
        response = c.get("/")
        self.assertContains(response, 'Who is more stupid',
                            status_code=200,
                            msg_prefix='пост не опубликован на главной странице',
                            html=False)
        response = c.get(f'/{self.user.username}/')
        self.assertContains(response, 'Who is more stupid',
                            status_code=200,
                            msg_prefix='пост не опубликован в профиле ползователя',
                            html=False)
        response = c.get(f'/{self.user.username}/{self.post.id}/')
        self.assertContains(response, 'Who is more stupid', status_code=200,
                            msg_prefix='пост не появился на отдельной странице поста',
                            html=False)

    def test_try_edit_post(self):
        c = self.client
        c.force_login(self.user)
        c.post(reverse('post_edit', args=[self.user.username, self.post.id],), {'text': 'Changed text', })
        response = c.get("/")
        self.assertContains(response, 'Changed text',
                            status_code=200,
                            msg_prefix='редактируемый пост не опубликован на главной странице',
                            html=False)
        response = c.get(reverse('profile', args=[self.user.username]))
        self.assertContains(response, 'Changed text',
                            status_code=200,
                            msg_prefix='редактируемый пост не опубликован в профиле ползователя',
                            html=False)
        response = c.get(reverse('post', args=[self.user.username, self.post.id],))
        self.assertContains(response, 'Changed text',
                            status_code=200,
                            msg_prefix='редактируемый пост не появился на отдельной странице поста',
                            html=False)

    def test_try_404(self):
        c = self.client
        response = self.client.get(f'/r2d2/')
        self.assertEqual(response.status_code, 404, msg="Не возвращается ошибка 404")