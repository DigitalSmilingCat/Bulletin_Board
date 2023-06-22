def add_login_to_context(request):
    return {'login': request.user.username if request.user.is_authenticated else None}