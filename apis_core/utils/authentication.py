from rest_framework.authentication import TokenAuthentication


# not used in APIS, but can be used in downstream projects
class TokenAuthSupportQueryString(TokenAuthentication):
    """
    Extend the TokenAuthentication class to support querystring authentication
    in the form of "http://www.example.com/?auth_token=<api_key>"
    """

    def authenticate(self, request):
        # Check if 'token_auth' is in the request query params.
        # Give precedence to 'Authorization' header.
        if (
            "api_key" in request.query_params
            and "HTTP_AUTHORIZATION" not in request.META
        ):
            return self.authenticate_credentials(request.query_params.get("api_key"))
        else:
            return super().authenticate(request)
