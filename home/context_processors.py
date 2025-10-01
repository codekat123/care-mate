from .models import Reservation


def global_context(request):
    if request.user.is_authenticated and request.user.role == "patient":
        patient = getattr(request.user, "patient", None)
        if patient:
            return {
                "count_of_notifications": Reservation.objects.filter(
                    patient=patient,
                    is_approved=True
                ).count()
            }
    return {}
