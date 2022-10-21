from Book.models import Post


def genredrop(request):
    post = list(Post.objects.all())
    book = list({i.Genre for i in post})
    context = {
        'book': book
    }
    return context
