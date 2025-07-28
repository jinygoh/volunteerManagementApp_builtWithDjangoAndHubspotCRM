class IPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip_address = request.META.get('REMOTE_ADDR')
        print(f"Request from IP address: {ip_address}")
        response = self.get_response(request)
        return response
