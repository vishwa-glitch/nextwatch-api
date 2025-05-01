class CloudFrontMiddleware:
    """
    Middleware to handle requests from CDNs or proxies.
    This middleware ensures that requests are properly processed
    by Django, even when the Host header contains a different domain.

    Note: This middleware is kept for compatibility but may not be needed
    with Render hosting.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process the request
        response = self.get_response(request)
        return response
