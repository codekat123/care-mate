from django.shortcuts import render , get_object_or_404 , redirect
from profile_users.models import DoctorProfile
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.views import View
from django.views.generic.edit import CreateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Reservation
from .forms import ReservationForm
from user_account.models import User
from django.db.models import Q
from django.contrib.postgres.search import SearchVector,SearchQuery,SearchRank

@method_decorator(login_required(login_url='user_account:login'),name='dispatch')
class HomeView(ListView):
     model = DoctorProfile
     template_name = 'home/home.html'
     context_object_name = "doctors"
     paginate_by = 10
     def get_queryset(self):
         return DoctorProfile.objects.filter(user__is_active=True)

     def get(self, *args, **kwargs):
         if self.request.user.role == 'doctor':
            return redirect('dashboard:dashboard')
         return super().get(*args, **kwargs)

@method_decorator(login_required(login_url='user_account:login'),name='dispatch')
class DoctorDetials(DetailView):
     model = DoctorProfile
     template_name = 'home/doctor_detail.html'
     context_object_name = 'doctor'

     def get_object(self,queryset=None):
          doctor_id = self.kwargs['doctor_id']
          return get_object_or_404(DoctorProfile,pk=doctor_id)
     
     def get_context_data(self,**kwargs):
          context = super().get_context_data(**kwargs)
          context['form'] = ReservationForm()
          return context
     
     def post(self,request,*args,**kwargs):
          self.object = self.get_object()
          form = ReservationForm(request.POST)
          if form.is_valid():
               reservation = form.save(commit=False)
               reservation.doctor = self.object
               reservation.patient = self.request.user.patient
               reservation.save()
               context = self.get_context_data()
               context['success'] = 'appointment booked successfully'
               return self.render_to_response(context)
          else:
            context = self.get_context_data(form=form)
            return self.render_to_response(context)

@method_decorator(login_required(login_url='user_account:login'),name='dispatch')
class SearchView(ListView):
    model = User
    template_name = 'home/search_resutls.html'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            search_query = SearchQuery(query)
            search_vector = (
                SearchVector("first_name", weight="A") +
                SearchVector("last_name", weight="A") +
                SearchVector("doctor__major", weight="A")
            )

            results = (
                User.objects.annotate(
                    search=search_vector,
                    rank=SearchRank(search_vector, search_query),
                )
                .filter(search=search_query)
                .order_by("-rank")
            )
            return results

        return User.objects.none()
       
    def get_context_data(self,*arg,**kwargs):
          context = super().get_context_data(**kwargs)
          return context

