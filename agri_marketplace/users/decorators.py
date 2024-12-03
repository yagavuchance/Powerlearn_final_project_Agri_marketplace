from django.http import HttpResponseForbidden

def supplier_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.profile.is_supplier:
            return HttpResponseForbidden("You do not have permission to access this page.")
        return view_func(request, *args, **kwargs)
    return wrapper
