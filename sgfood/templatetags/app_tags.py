from django import template
from ..models import LikeForComment, LikeForReview
register = template.Library()


@register.filter
def query_review_like(review, user):
    res = review.likeforreview_set.filter(user=user).exists()
    return res


@register.filter
def query_comment_like(comment, user):
    res = comment.likeforcomment_set.filter(user=user).exists()
    return res
