from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse, Http404
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm
from .models import Category, Restaurant, Review, LikeForReview, Comment, LikeForComment


def home(request):
    context = {'home': 'home1'}
    return render(request, 'sgfood/home.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            msg = 'Create '+username+' account successfully'
            messages.success(request, msg)

            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'sgfood/register.html', {'form': form})


def category(request):
    categories = Category.objects.all()
    return render(request, 'sgfood/category.html', {'categories': categories})


def restaurant_list(request, category_id):
    restaurants = Restaurant.objects.filter(category=category_id)

    context = {
        'restaurants': restaurants,
    }

    return render(request, 'sgfood/restaurant_list.html', context)


def restaurant_detail(request, category_id, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    reviews = Review.objects.filter(restaurant=restaurant).order_by("-pk")

    avg_rate = average_rating(reviews)

    context = {
        'restaurant': restaurant,
        'reviews': reviews,
        'avg_rate': avg_rate,
    }

    return render(request, 'sgfood/restaurant_detail.html', context)


def average_rating(reviews):
    avg_rating = 0
    if reviews.count() > 0:
        total = 0
        for review in reviews:
            total += review.rate
        avg_rating = total/reviews.count()
        return "{0:.2f}".format(avg_rating)
    else:
        return avg_rating


@login_required
def like_review(request):
    review_id = request.GET.get('review_id')
    preference = request.GET.get('preference')

    # [0]: unlike [1]:like
    if preference == "0":
        LikeForReview.objects.filter(
            review_id=review_id, user=request.user).delete()
        count = LikeForReview.objects.filter(review_id=review_id).count()
        return JsonResponse({'count': count, }, status=200)
    elif preference == "1":

        bExist = LikeForReview.objects.filter(
            review_id=review_id, user=request.user).exists()

        if not bExist:
            lr1 = LikeForReview(review_id=review_id, user=request.user)
            lr1.save()
            count = LikeForReview.objects.filter(review_id=review_id).count()
            response = JsonResponse({
                'status': 'succeeded ',
                'message': lr1.id,
                'count': count,
            }, status=200)
            return response

    response = JsonResponse({
        'status': 'failed',
        'message': 'LikeForReview sqlite exception',
    }, status=500)
    return response


@login_required
def like_comment(request):
    comment_id = request.GET.get('comment_id')
    preference = request.GET.get('preference')
    user = request.user

    # preference [0]:Unlike [1]:like
    if preference == "0":
        LikeForComment.objects.filter(
            comment_id=comment_id, user=user).delete()
        count = LikeForComment.objects.filter(comment_id=comment_id).count()

        return JsonResponse({'count': count, }, status=200)

    elif preference == "1":
        bExist = LikeForComment.objects.filter(
            comment_id=comment_id, user=user).exists()

        if not bExist:
            lc1 = LikeForComment(comment_id=comment_id, user=user)
            lc1.save()
            count = LikeForComment.objects.filter(
                comment_id=comment_id).count()

            response = JsonResponse({
                'status': 'succeeded',
                'message': lc1.id,
                'count': count,
            }, status=200)
            return response

    response = JsonResponse({
        'status': 'failed',
        'message': '',
    }, status=500)
    return response


def review_create(request):
    if request.user.is_authenticated:
        restaurant_id = request.GET.get("restaurant_id")
        description = request.GET.get("description")
        rate = request.GET.get("rate")

        review = Review(
            user=request.user,
            restaurant_id=restaurant_id,
            rate=int(rate),
            description=description
        )
        review.save()

        reviews = Review.objects.filter(
            restaurant_id=restaurant_id).order_by("-pk")

        content = {
            "reviews": reviews
        }

        return render(request, "sgfood/review.html", content)

        # return JsonResponse({"review_id": review.id}, status=200)
    else:
        return JsonResponse({"is_not_authenticated": True}, status=200)


def comment_create(request):
    if request.user.is_authenticated:
        review_id = request.GET.get("review_id")
        comment_id = request.GET.get("comment_id")
        description = request.GET.get("description")

        review = Review.objects.filter(id=review_id).first()

        if comment_id is not "":
            comment = Comment.objects.filter(id=comment_id).first()
        else:
            comment = None
        if review is not None:
            comment = Comment(
                user=request.user,
                review=review,
                description=description,
                reply=comment,
            )
            comment.save()

            restaurant = review.restaurant
            reviews = Review.objects.filter(
                restaurant=restaurant).order_by("-pk")
            content = {
                'reviews': reviews
            }
            return render(request, "sgfood/review.html", content)
        else:
            raise Http404("review id is not valid")
    else:
        return JsonResponse({"is_not_authenticated": True}, status=200)


def restaurant_rate(request):
    restaurant_id = request.GET.get('restaurant_id')

    reviews = Review.objects.filter(restaurant_id=restaurant_id)
    avg_rate = average_rating(reviews)
    review_count = reviews.count()

    response = JsonResponse({
        'review_count': review_count,
        'avg_rate': avg_rate,
    }, status=200)

    return response
