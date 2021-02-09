"""
-----------------------------------
Steps to create AuthToken Manually.
-----------------------------------
def create(self, request):
    try:
        user = User.objects.get(email=request.data.get('email'), password=request.data.get('password'))
        token = Token.objects.create(user=user)
        return Response({"Token":token.key, "Username":user.name,"Email":user.email})
    except :
        return Response({"Message":"Credentials are incorrect."})
"""
import urllib
import json
from django.core.exceptions import PermissionDenied
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from django.views.generic.edit import CreateView
from oauth2_provider.models import AccessToken
import requests
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, status
from . models import *
from . serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny
import json 
from django.conf import settings
import DaanpatraApp


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
        
    def retrieve(self, request, pk=None):
        response = {'message': 'Invalid Path.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, pk=None):
        response = {'message': 'Invalid Path.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, pk=None):
        response = {'message': 'Invalid Path.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk=None):
        response = {'message': 'Invalid Path.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

class Login(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    def post(self, request):
        response = requests.post("http://127.0.0.1:8000/o/token/", 
        data={
            'username':request.data.get('username'),
            'password':request.data.get('password'),
            'grant_type':'password',
            'client_id':settings.CLIENT_ID,
            'client_secret':settings.CLIENT_SECRET,
            'scope':'read'

        }
        
        )
        json_data = json.loads(response.text)
        token = json_data.get('access_token')
        token_data = AccessToken.objects.get(token=token)
        user = User.objects.get(uuid=token_data.user.uuid)
        
        user_details = {
            'Username':user.username,
            'Name':user.first_name + " " + user.last_name,
            'Email':user.email,
            'Birth Date':user.birth_date,
            'Role':user.role,
            'Permissions':user.get_all_permissions(),
            
        }

        user.password = ""
        user.save()
        if user_details:
            return Response({'Data':response.json(),'User':user_details,"Message":"login successfull.","Status":200})
        return Response({'Message':"Incorrect credentials.","Status":404})


class DriverActionsViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = DriverActionsSerializer

    def list(self, request, pk=None):
        response = {'message': 'Invalid Path.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, pk=None):
        response = {'message': 'Invalid Path.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def post(self, request, pk=None):
        response = {'message': 'Invalid Path.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        if request.user.has_perm('DaanpatraApp.can_remove_drivers'):
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"Message":"User Deleted"})
        else:
            raise PermissionDenied()


class UserActionsViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserActionsSerializer


class DonationViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer

    def retrieve(self, request, pk=None):
        response = {'message': 'Invalid Path.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def create(self, request):
        check = Donation.objects.filter(user=request.user.uuid).last()
        if check.donation_status == True:
            Product_Images = request.data.getlist('Product_Images')
            serializer = DonationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                for image in Product_Images:
                    ProductImages.objects.create(donation=Donation.objects.last(), images=image)
            return Response(serializer.data)
        else:
            return Response({"Message":"Last Donation has not been completed yet, You can only donate after the completion of last donation."})

class ProductImagesViewSet(viewsets.ModelViewSet):
    queryset = ProductImages.objects.all()
    serializer_class = ProductImagesSerializer

# class FundDonationViewSet(viewsets.ModelViewSet):
#     queryset = FundDonation.objects.all()
#     serializer_class = FundDonationSerializer

#     def create(self, request):
#         user = self.request.user
#         card_no = request.data.get('card_no')
#         exp_month = request.data.get('exp_month')
#         exp_year = request.data.get('exp_year')
#         cvc = request.data.get('cvc')
#         amount = request.data.get('amount')

#         import stripe
#         stripe.api_key = settings.STRIPE_API_KEY
        
#         card = stripe.Token.create(
#             card={
#                 "number": card_no,
#                 "exp_month": exp_month,
#                 "exp_year": exp_year,
#                 "cvc": cvc,
#             },
#         )

#         charge = stripe.Charge.create(
#             amount= int(amount) * 100,
#             currency="inr",
#             description="Donation",
#             source=card.id, # obtained with Stripe.js
#         )

#         import time
#         timestamp = charge.created + 19800
#         ts = time.gmtime(timestamp)
#         date = time.strftime("%Y-%m-%d", ts)
#         time = time.strftime("%H:%M:%S", ts)

#         FundDonation.objects.create(user=user, date=date, time=time, amount=int(amount))
#         if charge.status == 'succeeded':
#             return Response({"Message":"Fund Donated Successfully."})
#         else:
#             return Response({"Message":"Fund Transfer Failed."})

class DonationActionsViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all()
    serializer_class = DonationActionsSerializer

    def create(self, request):
        response = {'message': 'Invalid Path.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, pk=None):
        response = {'message': 'Invalid Path.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

 #-----------------------------TESTING PURPOSE-------------------------------

class CertificateViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all()
    serializer_class = CertificateSerializer

    def list(self, request):
        user_image = self.request.user.profile
        first_name = self.request.user.first_name
        last_name = self.request.user.last_name
        user_name = first_name + " " +last_name
        from PIL import Image, ImageDraw, ImageFont
        import pandas as pd
        pro = Image.open('/home/harsh/Projects/Daanpatra/media/' + str(user_image)) #25x25
        profile = pro.resize((1200,1500))
        im = Image.open("/home/harsh/Certificate/Sample.png")
        d = ImageDraw.Draw(im)
        location = (3000, 3000)
        font = ImageFont.truetype("/home/harsh/Certificate/04b_08/04B_08__.TTF", 250)
        d.text(location,user_name,fill=9,font=font)
        im.paste(profile,(550,700))
        im.save("certificate_"+user_name+".pdf")
        return Response({"Message":"Certificate Created Successfully."})

class TranslateViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all()
    serializer_class = TranslateSerializer

    def create(self, request):
        word = request.data.get('word')
        from googletrans import Translator
        translator = Translator()
        x = translator.translate(word, dest='hi')
        print(x.text)
        return Response({"Previous Word":word,"Tranlated Word":x.text})

class YouTubeVideoLinksViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all()
    serializer_class = YouTubeVideoLinksSerializer

    def list(self, request):
        channel_id='UCqwUrj10mAEsqezcItqvwEw'
        api_key = 'AIzaSyCn3jMunlfC7ekNtBxma6DzX9cMM3GiIYA'

        base_video_url = 'https://www.youtube.com/watch?v='
        base_search_url = 'https://www.googleapis.com/youtube/v3/search?'

        first_url = base_search_url+'key={}&channelId={}&part=snippet,id&order=date&maxResults=25'.format(api_key, channel_id)

        video_links = []
        url = first_url
        while True:
            inp = urllib.request.urlopen(url)
            resp = json.load(inp)

            for i in resp['items']:
                if i['id']['kind'] == "youtube#video":
                    video_links.append(base_video_url + i['id']['videoId'])

            try:
                next_page_token = resp['nextPageToken']
                url = first_url + '&pageToken={}'.format(next_page_token)
            except:
                break
        
        jsonStr = json.dumps(video_links)
        return Response({"Message":jsonStr})

    def create(self, request):
        vid_id = request.data.get('vid_id')
        if vid_id:
            response = requests.get('https://www.googleapis.com/youtube/v3/videos?part=snippet&id=' + vid_id + '&key=AIzaSyCn3jMunlfC7ekNtBxma6DzX9cMM3GiIYA')
            return Response(response.json())
        else:
            return Response({"Message":"Please Submit Video ID"})


class GoogleLoginViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all()
    serializer_class = GoogleLoginSerializer

    def list(self, request):
        try:
            import os 
            a = os.system('python /home/harsh/Projects/Daanpatra/DaanpatraApp/googlelogin.py')
            f = open('/home/harsh/Projects/Daanpatra/token.txt', 'r')
            token = f.read()

            response = requests.post('http://localhost:8000/auth/convert-token',
            data={
                'grant_type':'convert_token',
                'client_id':'04DpVJlIWfxGAMsNwMqJzkBpG654VpzCbnEz1meb',
                'client_secret':'XniDVIbxp8Ij1bI9tWiC9TE1AsdU3E40vbPLDP1xDfbXup5cE2lLPKJalbXs50yKMuPbqZMUubAAqyPXyVhxPyb44rFSASvgpy0p8uBC8OTzyM9o0fvdpt50uSWoQlVe',
                'token':token,
                'backend':'google-oauth2'
            }
            )
            f = open('/home/harsh/Projects/Daanpatra/token.txt', 'w')
            f.write("None")
            f.close()
            return Response("Logged in Successfully")
        except:
            return Response("Something went wrong, Please try again.")

class LogoutAPI(APIView):
    def post(self, request):
        response = requests.post('http://localhost:8000/o/revoke_token/',
        data={
            'token':request.auth,
            'client_id':settings.CLIENT_ID,
            'client_secret':settings.CLIENT_SECRET,
        }
        )
        if response.ok:
            return Response({'Message':"Logged Out Successfully."})
        return Response({'Message':"Already Logged Out."})


class DonationGalleryViewSet(viewsets.ModelViewSet):
    queryset = DonationGallery.objects.all()
    serializer_class = DonationGallerySerializer

    def retrieve(self, request, pk=None):
        response = {'message': 'Invalid Path.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)


    def create(self, request):
        if request.user.has_perm('DaanpatraApp.can_add_donation_gallery_images'):
            images = request.data.getlist('images')
            for image in images:
                DonationGallery.objects.create(images=image)
        else:
            raise PermissionDenied()

    def update(self, request, pk=None):
        response = {'message': 'Invalid Path.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, pk=None):
        response = {'message': 'Invalid Path.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        if request.user.has_perm('DaanpatraApp.can_remove_donation_gallery_images'):
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"Message":"Image Deleted"})
        else:
            raise PermissionDenied()

class UserAppLogin(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserAppLoginSerializer
    def post(self, request):
        response = requests.post("http://127.0.0.1:8000/o/token/", 
        data={
            'username':request.data.get('username'),
            'password':request.data.get('password'),
            'grant_type':'password',
            'client_id':settings.CLIENT_ID,
            'client_secret':settings.CLIENT_SECRET,
            'scope':'read'

        }
        
        )
        json_data = json.loads(response.text)
        token = json_data.get('access_token')
        token_data = AccessToken.objects.get(token=token)
        user = User.objects.get(uuid=token_data.user.uuid)
        
        user_details = {
            'Username':user.username,
            'Name':user.first_name + " " + user.last_name,
            'Email':user.email,
            'Birth Date':user.birth_date,
            'Role':user.role,
            'user':user,
            'Permissions':user.get_all_permissions(),
            
        }
        # user.otp = None
        # user.save()
        if user_details:
            return Response({'Data':response.json(),'User':user_details,"Message":"login successfull.","Status":200})
        return Response({'Message':"Incorrect credentials.","Status":404})


class OTP(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserAppSerializer
    def post(self, request):
        if request.data.get('username'):
            if User.objects.filter(username=request.data.get('username')).exists():
                user = User.objects.get(username=request.data.get('username'))
                import random
                otp = random.randint(111111, 999999)
                print(otp)
                user.set_password(str(otp))
                user.save()
                return Response({"Message":"OTP Sent",'status':200})
            else:
                return Response({"Message":"Contact Number Not Registered",'status':404})
        else:
            return Response({"Message":"Please enter contact number",'status':505})

class UserAppViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserAppSerializer

    def create(self, request):
        if User.objects.filter(username = request.data.get('contact')).exists():
            return Response({"Message":"Already Registered","status":500})
        else:
            user = User.objects.create(
                contact = request.data.get('contact'),
                username = request.data.get('contact'),
                # password = validated_data.get('password'),
                first_name = request.data.get('first_name'),
                last_name = request.data.get('last_name'),
            )
            # user.set_password(validated_data.get('password'))
            user.save()
            context = {
                "Message":"User Registered Successfully.",
                "status":200
            }
            return Response(context)



class TestViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all()
    serializer_class = TestSerializer

    def list(self, request):
        from pyfcm import FCMNotification
        push_service = FCMNotification(api_key="AAAANSv3sDw:APA91bEgoMXu74uPlgqSDlPMLhew0KceqnnLwqfPglk2uZ_PNd01EDbZ3TLx8cGP11lmbgqV3Vii3DIlH_fhTMhzcUdMUzOQjWcYowtOhlLVLPS3EkVHnmmXvhFAlJ8AOjNIfCIjZd")
        registration_id = ""
        message_title = "Uber update"
        message_body = "Hi john, your customized news for today is ready"
        result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

        print (result)
        # import webbrowser
        # base_url = "http://www.google.com/?#q="
        # query = input("Please enter your search query: ")
        # final_url = base_url + query
        # webbrowser.open_new(final_url)

        # import instaloader
        # bot = instaloader.Instaloader()
        # profile = instaloader.Profile.from_username(bot.context, 'poojatailor290')
        # posts = profile.get_posts()
        # # bot.download_profile('poojatailor290')


#-----------------------------TESTING PURPOSE-------------------------------