from django.test import TestCase
from django.contrib import auth
from mybrain.network.models import Comment, Follower, Post
from network.models import User
# Create your tests here.

class TestModel(TestCase):
    def test_should_create_user(self):
        user = User.objects.create_user(
            username='username',email='email@app/com'
        )
        user.set_password('123+789Asd')
        user.save()
        self.assertEqual(str(user),'username')

class TestModels(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass'
        )
        self.post = Post.objects.create(
            creater=self.user,
            content_text='This is a test post'
        )
        self.comment = Comment.objects.create(
            post=self.post,
            commenter=self.user,
            comment_content='This is a test comment'
        )
        self.follower = Follower.objects.create(user=self.user)
    
    def test_user_model(self):
        self.assertEqual(str(self.user), 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('testpass'))
    
    def test_post_model(self):
        self.assertEqual(str(self.post), 'Post ID: 1 (creater: testuser)')
        self.assertEqual(self.post.content_text, 'This is a test post')
    
    def test_comment_model(self):
        self.assertEqual(str(self.comment), 'Post: Post ID: 1 (creater: testuser) | Commenter: testuser')
        self.assertEqual(self.comment.comment_content, 'This is a test comment')
    
    def test_follower_model(self):
        self.assertEqual(str(self.follower), 'User: testuser')

class TestViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass'
        )
    
    def test_login_view(self):
        # Test login with correct credentials
        response = self.client.post(
            '/login/',
            {'username': 'testuser', 'password': 'testpass'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        
        # Test login with incorrect credentials
        response = self.client.post(
            '/login/',
            {'username': 'testuser', 'password': 'wrongpass'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid login')       

        
def setUp(self):
        # Create a test user
        self.test_user = User.objects.create_user(
            username='testuser', email='test@example.com', password='testpass'
        )
        self.test_user.save()
        # Create a post for the test user
        self.test_post = Post.objects.create(
            creater=self.test_user, content_text='test post'
        )
        self.test_post.save()
        # Create another test user
        self.test_user2 = User.objects.create_user(
            username='testuser2', email='test2@example.com', password='testpass'
        )
        self.test_user2.save() 

def test_unlike_post(self):
        # Test unlike a post as an authenticated user
        self.client.login(username='testuser', password='testpass')
        self.test_post.likers.add(self.test_user)
        self.test_post.save()
        response = self.client.put(f'/post/{self.test_post.id}/unlike/', follow=True)
        self.assertEqual(response.status_code, 204)
        self.assertNotIn(self.test_user, self.test_post.likers.all())
        # Test unlike a post as an unauthenticated user
        self.client.logout()
        response = self.client.put(f'/post/{self.test_post.id}/unlike/', follow=True)
        self.assertEqual(response.status_code, 302)


def test_user_serialize(self):
        # create a user to serialize
        user = User.objects.create_user(
            username='username',email='email@app/com', first_name='First', last_name='Last'
        )
        user.set_password('123+789Asd')
        user.save()

        # serialize the user and check that the serialization is correct
        serialized_user = user.serialize()
        self.assertEqual(serialized_user['id'], user.id)
        self.assertEqual(serialized_user['username'], user.username)
        self.assertEqual(serialized_user['profile_pic'], user.profile_pic.url)
        self.assertEqual(serialized_user['first_name'], user.first_name)
        self.assertEqual(serialized_user['last_name'], user.last_name)

def test_post_img_url(self):
        # create a user to use as the creater of the post
        user = User.objects.create_user(
            username='username',email='email@app/com'
        )
        user.set_password('123+789Asd')
        user.save()

        # create a new post with an image
        post = Post.objects.create(
            creater=user,
            content_text='This is a test post',
            content_image='posts/test.jpg'
        )

        # check that the img_url method returns the correct URL for the post image
        self.assertEqual(post.img_url(), 'posts/test.jpg')

def test_post_append(self):
        # create a user to use as the creater of the post
        user = User.objects.create_user(
            username='username',email='email@app/com'
        )
        user.set_password('123+789Asd')
        user.save()

        # create a new post
        post = Post.objects.create(
            creater=user,
            content_text='This is a test post'
        )

        # use the append method to add a new attribute to the post object
        post.append('test_attr', 'test_value')

        # check that the new attribute was added to the post object
        self.assertEqual(post.test_attr, 'test_value')


def test_comment_serialize(self):
        # create a user to use as the creater of the post and the commenter
        user = User.objects.create_user(
            username='username',email='email@app/com'
        )
        user.set_password('123+789Asd')
        user.save()

        # create a new post
        post = Post.objects.create(
            creater=user,
            content_text='This is a test post'
        )

        # create a new comment on the post
        comment = Comment.objects.create(
            post=post,
            commenter=user,
            comment_content='This is a test comment'
        )
         # serialize the comment and check that the serialization is correct
        serialized_comment = comment.serialize()
        self.assertEqual(serialized_comment['id'], comment.id)
        self.assertEqual(serialized_comment['commenter'], user.serialize())
        self.assertEqual(serialized_comment['body'], comment.comment_content)
        self.assertEqual(serialized_comment['timestamp'], comment.comment_time.strftime("%b %d %Y, %I:%M %p"))