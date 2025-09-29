from .models import Reservation


def global_context(request):
    if request.user.is_authenticated:
        if request.user.role == "patient":
            return {
                "count_of_notifications": Reservation.objects.filter(patient=request.user.patient,is_approved=True).count(),
            }
    return {}