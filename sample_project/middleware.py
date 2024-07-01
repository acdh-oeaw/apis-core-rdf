class XRealIPMiddleware():
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if "HTTP_X_REAL_IP" in request.META:
            request.META["HTTP_X_PROXY_REMOTE_ADDR"] = request.META["REMOTE_ADDR"]
            parts = request.META["HTTP_X_REAL_IP"].split(",", 1)
            request.META["REMOTE_ADDR"] = parts[0]
        return self.get_response(request)
