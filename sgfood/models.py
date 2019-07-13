from django.db import models
from django.contrib.auth.models import User


string_format_2 = '{0} - {1}'
string_format_3 = '{0} - {1} - {2}'


class Category(models.Model):
    description = models.CharField(max_length=255)

    def __str__(self):
        return string_format_2.format(self.id, self.description)


class Restaurant(models.Model):
    name = models.CharField(max_length=20)
    address = models.CharField(max_length=50)

    # many restaurants to one category
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return string_format_3.format(self.id, self.name, self.category)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    rate = models.IntegerField(default=0)
    description = models.CharField(max_length=255)

    def get_comments(self):
        return self.comment_set.filter(reply=None)

    def __str__(self):
        return string_format_3.format(self.restaurant, self.description, self.user)


class LikeForReview(models.Model):
    # similar to composite primary key
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


# Note: one user can leave comment on one review many times
class Comment(models.Model):
    # many comments to one review
    review = models.ForeignKey(Review, on_delete=models.CASCADE)

    # many comments to one user
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    description = models.CharField(max_length=255)

    reply = models.ForeignKey('Comment', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return string_format_3.format(self.review, self.description, self.user)


class LikeForComment(models.Model):
    # similar to composite primary key
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
