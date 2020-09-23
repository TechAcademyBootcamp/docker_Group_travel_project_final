from django.shortcuts import render, redirect,get_object_or_404
from django.views.generic import ListView,CreateView,DetailView,View
from Hotels.models import Hotel,HotelAmenities,PoliciesSubFeatures,RoomAmenities,Reservation,RoomType,Policies,Reviews,ReviewFields,ReviewRating,\
    HotelImages,SavedArticle
from Account.models import User
from django.urls import reverse_lazy
from django.views.generic.edit import FormMixin
from django.contrib.sites.models import Site
from django.conf import settings
import stripe
from django.core.paginator import Paginator
from django.contrib import messages
from datetime import date,timedelta
from Hotels.tasks import send_at_time
from django.http import HttpResponse


stripe.api_key = settings.STRIPE_SECRET_KEY

class HotelsListView(ListView):
    model = Hotel
    template_name = 'hotels.html'
    paginate_by = 5
    context_object_name = 'hotels'

    def get_context_data(self, **kwargs):
        context = super(HotelsListView, self).get_context_data(**kwargs)
        hotel_amenities = HotelAmenities.objects.all()
        room_amenities= RoomAmenities.objects.all()
        context['room_amenities']=room_amenities
        context['hotel_amenities'] = hotel_amenities
        PoliciesSub = PoliciesSubFeatures.objects.all()
        context['PoliciesSub'] = PoliciesSub
        current_site = Site.objects.last()
        context['url'] = f"{self.request.get_host()}{reverse_lazy('api_hotel:hotel')}"
        page = self.request.GET.get('page', 1) if self.request.GET.get('page', 1) != '' else 1
        data = self.get_queryset()
        if data:
            paginator = Paginator(data, self.paginate_by)
            results = paginator.page(page)
            index = results.number - 1
            max_index = len(paginator.page_range)
            start_index = index - 5 if index >= 5 else 0
            end_index = index + 5 if index <= max_index - 5 else max_index
            context['page_range'] = list(paginator.page_range)[start_index:end_index]
        return context



class HotelsSinglePage(DetailView):
    model = Hotel
    template_name = 'single_page.html'

    def get_context_data(self, **kwargs):
        allRatingsForHotel = ReviewRating.objects.filter(hotel=self.get_object().pk)
        ratings = {
        }
        count=0
        for objects in allRatingsForHotel:
            for field in objects.review_field.all():
                if field not in ratings:
                    ratings[field]=objects.rating_point
                else:
                    ratings[field]+=objects.rating_point
                    count+=1
        delivery_count = (count/6)+1
        for key,value in ratings.items():
            ratings[key]=float( '%.1f'%((value/delivery_count)))
        context = super(HotelsSinglePage, self).get_context_data(**kwargs)
        hotelImages=HotelImages.objects.filter(hotel__id=self.get_object().pk)[:3]
        context['images']=hotelImages
        context['ratings']=ratings
        hotels = Hotel.objects.all()[:4]
        context['nearest_hotels'] = hotels
        policies = Policies.objects.all()
        context['policyy']=policies
        reviews = Reviews.objects.all()[:4]
        context['reviews'] = reviews
        context['review_count']=Reviews.objects.filter(reservation__hotel__id=self.get_object().pk).count()
        # context['review_fields']=ReviewFields.objects.all()
        return context


class ReservePage(FormMixin,DetailView):
    template_name = 'payment.html'
    model = RoomType
    context_object_name = 'room_type'

    def post(self,request, *args, **kwargs):
        if request.method == 'POST':
            print('helllllllllllllooooooooooooooo')
            token = request.POST.get('stripeToken', False)
            if token:
                customer = stripe.Customer.create(
                    email=request.user.email,
                    name=request.user.username,
                    source=token
                )
                charge = stripe.Charge.create(
                    customer=customer,
                    amount=16000,
                    currency='usd',
                    description='Example charge',
                )
                start_date=request.GET.get('first_date',date.today())
                fin_date=request.GET.get('second_date',date.today()+timedelta(1))
                day_count = request.GET.get('total_days',1)
                hotel = Hotel.objects.filter(id=request.GET.get('HotelId')).first()
                price = (int(self.get_object().price)*int(day_count))
                reservation = Reservation.objects.create(
                    reservation_start_date=start_date,
                    reservation_fin_date=fin_date,
                    price=float(price),
                    day_count=day_count,
                    room_type=self.get_object(),
                    user=request.user,
                    hotel=hotel,
                )
                messages.success(request, 'Paid successfull!')
                url=f"{self.request.get_host()}{reverse_lazy('hotels_app:hotels-reviews')}"
                send_at_time(request.user.email, reservation.id, url, fin_date)
                return redirect(reverse_lazy('hotels_app:hotels'))
        messages.success(request, 'Token not found!')
        return redirect(reverse_lazy('hotels_app:hotels'))

    def get_context_data(self, **kwargs):
        context = super(FormMixin,self).get_context_data(**kwargs)
        hotel = Hotel.objects.filter(pk=self.request.GET.get('HotelId')).first()
        context['hotel'] = hotel
        return context


class ReviewSendView(View):
    review_fields = ReviewFields.objects.all()
    user = User.objects.all()[0]
    context = {
        'review_fields': review_fields,
        'user': user,
    }
    def get(self,request):
        reservation = Reservation.objects.filter(pk=request.GET.get('reservation_id')).first()
        self.context['reservation']=reservation
        return render(request, 'review.html', self.context)

    def post(self, request, *args, **kwargs):
        reviewFields = ReviewFields.objects.all()
        for key, value in request.POST.items():
            if reviewFields.filter(title=key):
                reviewRating = ReviewRating.objects.create(
                    rating_point=value,
                    hotel=Hotel.objects.filter(name=request.POST.get('hotel-name')).first()
                )
                reviewField_for_Save = ReviewFields.objects.filter(title=key).first()
                reviewRating.review_field.add(reviewField_for_Save)
                reviewRating.save()
        my_reservation = Reservation.objects.filter(pk=request.POST.get('reservation')).first()
        review = Reviews.objects.create(
            subject=request.POST.get('my-text'),
            reservation=my_reservation
        )
        review.save()
        return render(request,'review.html',self.context)

class SavedHotelView(View):
    def get(self,*args,**kwargs):
        hotel_id = kwargs.get('pk')
        message = 'Hotel added to wishlist.'
        hotel=get_object_or_404(Hotel,id=hotel_id)
        if self.request.user.is_authenticated:
            save_hotel,created= SavedArticle.objects.get_or_create(user=self.request.user,hotel=hotel)
            if not created:
                message='Hotel was added already'
            response = HttpResponse(message)
        else:
            saved_hotels = self.request.COOKIES.get('saved_hotels', '')
            if str(hotel_id) not in saved_hotels.split(';'):
                saved_hotels += str(hotel_id) + ";"
            response = HttpResponse(message)
            response.set_cookie('saved_hotels', saved_hotels)
            # messages.success(self.request, message)
        return response

class SavedHotelListView(ListView):
    model = Hotel
    template_name = 'saved_hotels.html'
    context_object_name = 'hotels'
    paginate_by = 4
    def get_queryset(self, ):
        if self.request.user.is_authenticated:
            user_saved_articles_ids = self.request.user.saved_articles.values_list('hotel__id', flat=True)
            queryset = super().get_queryset().filter(id__in=user_saved_articles_ids)
            print(queryset)
            print(user_saved_articles_ids)
            return queryset
        else:
            saved_hotels = self.request.COOKIES.get('saved_hotels')
            if saved_hotels:
                saved_hotel_ids = [int(id) for id in saved_hotels.split(';') if id and id != 0]
                queryset = super().get_queryset()
                return queryset.filter(id__in=saved_hotel_ids)
            return None



