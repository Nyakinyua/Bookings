from django.db import models
from django.conf import settings
from pyuploadcare.dj.models import ImageField
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.
CATEGORY_CHOICES = (
    ('SC', 'Skin Care'),
    ('HC', 'Hair Care'),
    ('PC', 'Personal Care'),
    ('F', 'Fragrances'),
    ('MK', 'Makeup'),
    ('MP', 'Manicure $ Pedicure'),
    ('S', 'suntan')
    
)
LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)


class Item(models.Model):
    title = models.CharField(max_length=100)
    image = ImageField(blank=True, manual_crop='')
    price = models.FloatField()
    discount_price = models.FloatField(blank=True,null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2, default='S')
    label = models.CharField(choices=LABEL_CHOICES, max_length=1, default='P')
    slug = models.SlugField(default=None,null=True)
    description = models.TextField(default=None,null=True)
    quantity = models.IntegerField(default=1)
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('detail',kwargs={
            'slug':self.slug
        })


class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Salonposts(models.Model):
    name = models.CharField(max_length=30)
    pic = ImageField(blank=True, manual_crop='')
    price = models.FloatField()
    date = models.DateTimeField()

    @classmethod
    def get_one_post(cls, id):
        one_post = cls.objects.get(id=id)
        return one_post
    
    @classmethod
    def get_post_id(cls,postId):
        post_id=cls.objects.filter(id=postId)
        return post_id
    


class Comments(models.Model):
    comment = models.TextField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Salonposts, on_delete=models.CASCADE)

    def save_comment(self):
        return self.save()

    def __str__(self):

        return self.comment

    def get_comment(cls,id):
        comments = cls.objects.filter(salonpost_id__in=id)
        return comments
    
    
