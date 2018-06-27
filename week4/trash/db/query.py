from datetime import datetime

from django.db.models import Q, Count, Avg
from pytz import UTC

from db.models import User, Blog, Topic


def create():
    user1 = User(first_name='u1', last_name='u1')
    user1.save()
    user2 = User(first_name='u2', last_name='u2')
    user2.save()
    user3 = User(first_name='u3', last_name='u3')
    user3.save()

    blog1 = Blog(title='blog1', author=user1)
    blog1.save()
    blog2 = Blog(title='blog2', author=user1)
    blog2.save()

    blog1.subscribers.add(user1, user2)
    blog2.subscribers.add(user2)

    topic1 = Topic(title='topic1', blog=blog1, author=user1)
    topic1.save()
    topic2 = Topic(title='topic2_content', blog=blog1, author=user1, created='2017-01-01')
    topic2.save()

    topic1.likes.add(user1, user2, user3)


def edit_all():
    users = User.objects.all().update(first_name='uu1')


def edit_u1_u2():
    users = User.objects.filter(Q(first_name='u1') | Q(first_name='u2')).update(first_name='uu1')


def delete_u1():
    user = User.objects.get(first_name='u1')
    user.delete()


def unsubscribe_u2_from_blogs():
    user = User.objects.get(first_name='u2')
    blogs = Blog.objects.filter(subscribers=user)
    for blog in blogs:
        blog.subscribers.remove(user)



def get_topic_created_grated():
    topic = Topic.objects.filter(created__gt='2018-01-01')



def get_topic_title_ended():
    topic = Topic.objects.filter(title__endswith='content')


def get_user_with_limit():
    users = User.objects.all().order_by('-id')[:1]


def get_topic_count():
    pass
    # topic_count = Topic
    # topic_count = Topic.objects.all().values('blog').annotate(count=count('id')).order_by('count')


def get_avg_topic_count():
    pass


def get_blog_that_have_more_than_one_topic():
    blogs = Topic.objects.annotate(count_blogs=Count('blog')).filter(count_blogs__gt=1)


def get_topic_by_u1():
    topic_by_u1 = Topic.objects.filter(author__first_name='u1')


def get_user_that_dont_have_blog():
    pass


def get_topic_that_like_all_users():
    pass


def get_topic_that_dont_have_like():
    pass
