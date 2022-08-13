from django.shortcuts import redirect

from custom_admin.models import AdminUser


class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not (
            request.user.is_authenticated and AdminUser.objects.filter(user=request.user).exists()
        ):
            return redirect("custom-admin-login")
        return super().dispatch(request, *args, **kwargs)
