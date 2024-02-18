# middleware for setting the default branch in the session if it's not set yet

def set_default_branch_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before the view (and later middleware) are called.
        if 'branch' not in request.session:
            request.session['branch'] = 'Israel'

        # Code to be executed for each request/response after the view is called.
        response = get_response(request)

        return response

    return middleware
