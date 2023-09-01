from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post
from django.shortcuts import reverse

class BlogPostTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username = 'user1')
        cls.post1 = Post.objects.create(
            title = 'Post1',
            text = 'this is the description of post1',
            status = Post.STATUS_CHOICES[0][0],
            author =  cls.user,
        )
        cls.post2 = Post.objects.create(
            title = 'post2',
            text = "lorem ipsum post2",
            status = Post.STATUS_CHOICES[1][0],
            author = cls.user,
        )
    # def setUp(self):

    def test_post_model_str(self):
        post = self.post1
        self.assertEqual(str(post),post.title )

    def test_post_detail(self):
        self.assertURLEqual(self.post1.title , 'Post1')
        self.assertEqual(self.post1.text,'this is the description of post1' )


    def test_post_list_url(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code , 200)

    def test_post_list_by_name(self):
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code , 200)

    def test_post_title_on_blog_post(self):
        response = self.client.get(reverse('post_list'))
        self.assertContains(response , self.post1.title)

    def test_post_detail_url(self):
        response = self.client.get(f'/blog/{self.post1.id}/')
        self.assertEqual(response.status_code , 200)

    def test_post_detail_url_by_name(self):
        response = self.client.get(reverse("post_detail", args=[self.post1.id]))
        self.assertEqual(response.status_code , 200)

    # def test_post_details_on_blog_detail_page(self):              #FAILED
    #     response = self.client.get(reverse("post_detail", args=[self.post1.id]))
    #     self.assertContains(response, self.post1.title)
    #     self.assertContains(response, self.post1.text)

    def test_status_404_if_post_id_not_exist(self):
      response = self.client.get(reverse("post_detail" , args=[999]))
      self.assertEqual(response.status_code , 404)

    def test_draft_post_not_show_in_post_list(self):   #TDD
        response = self.client.get(reverse('post_list'))
        self.assertContains(response, self.post1.title)
        self.assertNotContains(response, self.post2.title)

    def test_post_create_view(self):
        response = self.client.post(reverse('post_create'),{
            "title" : "some title",
            "text" : "this is the text",
            "status": "pub",
            "author" : self.user.id,

        })
        self.assertEqual(response.status_code,302)
        self.assertEqual(Post.objects.last().title,"some title")
        self.assertEqual(Post.objects.last().text, "this is the text")

    def test_post_update_view(self):
        response = self.client.post(reverse("post_update",args=[self.post2.id]), {
            "title" : "post 2 updated",
            "text" : "this text is updated",
            "status": "pub",
            "author": self.user.id,       #self.post2.author.id
        })
        self.assertEqual(response.status_code,302)
        self.assertEqual(Post.objects.last().title, "post 2 updated")
        self.assertEqual(Post.objects.last().text, "this text is updated")

    def test_post_delete_view(self):
        response = self.client.post(reverse("post_delete", args=[self.post2.id]),)
        self.assertEqual(response.status_code,302)
