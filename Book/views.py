from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView
)
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
import urllib
from django.utils.encoding import smart_str
import mimetypes
from wsgiref.util import FileWrapper
from pathlib import Path
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, reverse, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, Http404, FileResponse
from .models import Post
from django.core.mail import send_mail
from django.views import View
import stripe
from django.conf import settings
import json
import os

stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = "whsec_73d9ba2cc144dfdb265bf329b1cbf35d5bee02edd4713ef9f7857a724a8821dd"

YOUR_DOMAIN = 'http://127.0.0.1:8000/'
# from django.views.generic import DetailView


def home(request):
    posts = list(Post.objects.all())
    posts = [posts[i:i+4] for i in range(0, len(posts), 4)]
    tops = Post.objects.all()
    top = [[i, i.upvotes.count()] for i in tops]
    top = sorted(top, key=lambda l: -1*l[1])
    # ans = [i[0] for i in top]
    ans = [i[0] for i in top[0:8]]
    # ans = top[0:8]
    print("mai hi hoon re")
    print(ans)
    context = {
        'posts': posts,
        'top': ans,
    }
    return render(request, 'Book/home.html', context)


# def download(request, path):
#     file_path = os.path.join(settings.MEDIA_ROOT, path)
#     print(path)
#     print(":):):):):):)")
#     if os.path.exists(file_path):
#         with open(file_path, 'rb')as f:
#             response = HttpResponse(
#                 f.read(), content_type='application/File')
#             response['Content-Disposition'] = 'attachment; filename' + \
#                 os.path.basname(file_path)
#             return response

#     raise Http404


def search(request):
    query = request.GET['query']
    posts = Post.objects.filter(Book_name__icontains=query)
    count = posts.count()
    print(count)
    b = True
    if(count == 0):
        b = False
    posts = [posts[i:i+3] for i in range(0, len(posts), 3)]
    context = {
        'posts': posts,
        'count': b,
    }
    return render(request, 'Book/search.html', context)


def gen(request, pk):
    # book = request.GET['book']
    print(pk)
    posts = Post.objects.filter(Genre__icontains=pk)
    count = posts.count()
    posts = [posts[i:i+3] for i in range(0, len(posts), 3)]
    context = {
        'posts': posts,
        'pk': pk
    }
    return render(request, 'Book/genres.html', context)


def report(request):
    if request.method == "POST":
        message_name = request.POST['message-name']
        message_email = request.user.email
        message = request.POST['message']
        print(request.POST)
        send_mail(
            message_name,
            message,
            message_email,
            ['elibrarybookalicious@gmail.com'],
        )
        return HttpResponseRedirect(reverse('book-detail', args=(request.POST['id'],),))
        # return render(request, 'Book/post_detail.html/request.POST['id']', {'message_name': message_name})
    else:
        return render(request, 'Book/post_detail.html', {})


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post


def calculate_order_amount(items):
    # Replace this constant with a calculation of the order's amount
    # Calculate the order total on the server to prevent
    # people from directly manipulating the amount on the client
    return 1400


def create_payment(request, id, type):
    print(request.body)
    print("kkdajaj")
    Amount = 0
    if type == 1:
        Amount = Post.objects.get(pk=id).SPrice
    else:
        Amount = Post.objects.get(pk=id).HPrice
    try:
        print(Amount)
        # print(request.data)
        # Create a PaymentIntent with the order amount and currency
        # Amount = 1500,

        intent = stripe.PaymentIntent.create(
            amount=Amount*100,
            currency='INR',
            metadata={
                # 'product_id': request.user.id,
                'id': id,
                'user': request.user.id,
                'type': type,
                'email': request.user.email
            },
            automatic_payment_methods={
                'enabled': True,
            },
        )
        return JsonResponse({
            'clientSecret': intent['client_secret']
        })
    except Exception as e:
        print("jadjhc")
        print(e)
        return JsonResponse({'error': str(e)})
        # return HttpResponse(status=200)

    #     print(e)


@csrf_exempt
def webhook(request):
    print("aa gaya uffffffffffffffffffffffff")
    if request.method == 'POST':
        print("KKKKKKKKK")
        event = None
        payload = request.body

        try:
            event = json.loads(payload)
        except:
            print('⚠️  Webhook error while parsing basic request.' + str(e))
            return JsonResponse({'success': False})
        if endpoint_secret:
            # Only verify the event if there is an endpoint secret defined
            # Otherwise use the basic event deserialized with json
            sig_header = request.headers.get('stripe-signature')
            try:
                event = stripe.Webhook.construct_event(
                    payload, sig_header, endpoint_secret
                )
            except stripe.error.SignatureVerificationError as e:
                print('⚠️  Webhook signature verification failed.' + str(e))
                return JsonResponse({'success': False})

        # Handle the event
        if event and event['type'] == 'payment_intent.succeeded':
            print(event)
            # contains a stripe.PaymentIntent
            payment_intent = event['data']['object']

            print('Payment for {} succeeded'.format(payment_intent['amount']))
            Id = int(payment_intent['metadata']['id'])
            mail = int(payment_intent['metadata']['user'])
            print(mail)
            Book = Post.objects.get(pk=Id)
            tomail = User.objects.get(pk=mail).email
            print(tomail)
            email = EmailMessage(
                "Here is your file !!",
                "Thanks for the Purchase,We Hope to see you again...Enjoy Reading",
                "elibrarybookalicious@gmail.com",
                [tomail]
            )

            # file = Book.File
            file_name = Post.objects.get(
                pk=Id).File.url.rsplit('/', 1)[-1]
            # email.attach(Book.Book_name, Book.read(),)
            file_path = settings.MEDIA_ROOT + '/'+'media'+'/' + 'files'+'/'+file_name
            email.attach_file(file_path)
            email.send()
            # send_mail(
            #     "Here is your product",
            #     "Thanks for purchase",
            #     "elibrarybookalicious@gmail.com",
            #     ["priyanshumavale@gmail.com"],
            # )
            print("mail pathavla")
            Copy_Type = payment_intent['metadata']['type']
            Copy_Id = payment_intent['metadata']['id']
            # User = int(payment_intent['metadata']['user'])

            print(Copy_Type)
            print(Copy_Id)
            if Copy_Type == '1':

                # r = int(Copy_Id)
                # if(Post.objects.get(pk=r).downloads.filter(username=request.user).count() == 0):
                # b1 = Post.objects.get(pk=Copy_Id)
                # b1.downloads.add(User)
                # b1.save()
                # print('done')
                # return render(request, 'Book/home.html')
                # # return JsonResponse({'bool': True})
                # # else:
                # #     return JsonResponse({'bool': False})

                # path = Post.objects.get(pk=Copy_Id).File.url
                # wrapper = FileWrapper(open(path, "r"))
                # content_type = mimetypes.guess_type(path)[0]

                # response = HttpResponse(wrapper, content_type=content_type)
                # # not FileField instance
                # response['Content-Length'] = os.path.getsize(path)
                # response['Content-Disposition'] = 'attachment; filename=%s' % \
                #     smart_str(os.path.basename(path))  # same here

                # return response
                file_name = Post.objects.get(
                    pk=Copy_Id).File.url.rsplit('/', 1)[-1]
                file_path = settings.MEDIA_ROOT + '/'+'media'+'/' + 'files'+'/'+file_name
                with open(file_path, 'rb') as fopen:
                    q = fopen.read()
                    print(q.decode())
                response = HttpResponse(open(file_path, 'rb').read())
                print(response)
                response['Content-Type'] = 'text/plain'
                response['Content-Disposition'] = 'attachment; filename=DownloadedText.pdf'
                return response
                file_wrapper = FileWrapper(open(file_path, 'rb'))
                print(file_wrapper)
                file_mimetype = mimetypes.guess_type(file_path)
                response = HttpResponse(
                    file_wrapper, content_type=file_mimetype)
                response['X-Sendfile'] = file_path
                response['Content-Length'] = os.stat(file_path).st_size
                response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(
                    file_path)
                print(response['Content-Disposition'])
                return response

                # request.session['id'] = Copy_Id
                # print(request.session['id'])
                # request.session['type'] = Copy_Type
                # URL = Post.objects.get(pk=Copy_Id).File.url
                # print(URL)
                # print("mi alo")

                # BASE_DIR = Path(__file__).resolve().parent.parent
                # file_path = os.path.join(settings.MEDIA_ROOT, URL)
                # file_path = r"C:\Users\acer\Desktop\Bookalicious\D\Q\media\media\files\Rich_Dad_Poor_Dad__PDFDrive_.pdf"
                # file_path = "C:\Users\acer\Desktop\Bookalicious\D\Q\media\media\files\Bird_Box_Malerman_Josh_z-lib.org.epub"
                # print(":):):):):):)")
                # if os.path.exists(file_path):
                # print("aalo")
                # # file_path = settings.MEDIA_ROOT + URL

                # # print(file_path)

                # file_path = os.path.join(settings.MEDIA_ROOT, URL)
                # print(file_path)
                # if os.path.exists(file_path):
                #     with open(file_path, 'rb') as fh:
                #         response = HttpResponse(
                #             fh.read(), content_type="application/vnd.ms-excel")
                #         response['Content-Disposition'] = 'inline; filename=' + \
                #             os.path.basename(file_path)
                #         return response
                # raise Http404

                # file_wrapper = FileWrapper(open(file_path, 'rb'))
                # file_mimetype = mimetypes.guess_type(file_path)
                # response = HttpResponse(
                #     file_wrapper, content_type=file_mimetype)
                # response['X-Sendfile'] = file_path
                # response['Content-Length'] = os.stat(file_path).st_size
                # response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(
                #     file_path)
                # print(response)
                # return response
                # with open(file_path, 'rb')as f:
                #     response = HttpResponse(
                #         f.read(), content_type='application/File')
                #     response['Content-Disposition'] = 'attachment; filename' + \
                #         os.path.basename(file_path)

                # return response

                # raise Http404

                return HttpResponseRedirect(reverse('download', args=(URL,)))
            # Then define and call a method to handle the successful payment intent.
            # handle_payment_intent_succeeded(payment_intent)
        elif event['type'] == 'payment_method.attached':
            # contains a stripe.PaymentMethod
            payment_method = event['data']['object']
            # Then define and call a method to handle the successful attachment of a PaymentMethod.
            # handle_payment_method_attached(payment_method)
        else:
            # Unexpected event type
            print('Unhandled event type {}'.format(event['type']))

        return JsonResponse({'success': True})


def success(request, id, type):
    print("pi punha yein")

    # id = request.session['id']
    # type = request.session['type']
    # context = {
    #     'p': Post.objects.get(id=id)
    # }
    Book = Post.objects.get(id=id)
    if(Post.objects.get(pk=id).downloads.filter(username=request.user).count() == 1):
        valid = 1
    else:
        valid = 0

    context = {
        'valid': valid,
        'id': id,
        'type': type,
        'Book': Book
    }
    return render(request, 'Book/success.html', context)


def go(request, id, type):
    if type == 1:
        Amount = Post.objects.get(pk=id).SPrice
    else:
        Amount = Post.objects.get(pk=id).HPrice
    context = {
        'pk': Amount,
        'id': id,
        'type': type
    }
    return render(request, 'Book/checkout.html', context)


class upvote(View):
    def post(self, request):
        print(request.POST)
        r = request.POST['book']
        print(r)
        if(Post.objects.get(pk=r).upvotes.filter(username=request.user).count() == 0):
            b1 = Post.objects.get(pk=r)
            b1.upvotes.add(request.user)
            b1.save()
            return JsonResponse({'bool': True})
        else:
            Post.objects.get(pk=r).upvotes.remove(request.user)
            return JsonResponse({'bool': False})


class downloads(View):
    def post(self, request):
        r = request.POST['book']
        if(Post.objects.get(pk=r).downloads.filter(username=request.user).count() == 0):
            b1 = Post.objects.get(pk=r)
            b1.downloads.add(request.user)
            b1.save()
            return JsonResponse({'bool': True})
        else:
            return JsonResponse({'bool': False})


class reads(View):
    def post(self, request):
        r = request.POST['book']
        if(Post.objects.get(pk=r).reads.filter(username=request.user).count() == 0):
            b1 = Post.objects.get(pk=r)
            b1.reads.add(request.user)
            b1.save()
            return JsonResponse({'bool': True})
        else:
            return JsonResponse({'bool': False})


class fav(View):
    def post(self, request):
        print(request.POST)
        r = request.POST['book']
        print(r)
        if(Post.objects.get(pk=r).fav.filter(username=request.user).count() == 0):
            b1 = Post.objects.get(pk=r)
            b1.fav.add(request.user)
            b1.save()
            return JsonResponse({'bool': True})
        else:
            Post.objects.get(pk=r).fav.remove(request.user)
            return JsonResponse({'bool': False})


# class go(TemplateView):
#     template_name = 'Book/checkout.html'
