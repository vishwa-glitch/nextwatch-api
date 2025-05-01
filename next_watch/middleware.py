class CloudFrontMiddleware:
    """
    Middleware to handle requests from CDNs or proxies.
    This middleware ensures that requests are properly processed
    by Django, even when the Host header contains a different domain.

    Updated to handle CORS headers for Render hosting.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process the request
        response = self.get_response(request)

        # Ensure CORS headers are properly set for credentials
        if 'Access-Control-Allow-Origin' in response and 'Access-Control-Allow-Credentials' not in response:
            response['Access-Control-Allow-Credentials'] = 'true'

        # Add debugging headers to help troubleshoot CORS issues
        if 'HTTP_ORIGIN' in request.META:
            origin = request.META.get('HTTP_ORIGIN')
            # Log the origin for debugging
            print(f"Request origin: {origin}")
            print(f"CORS headers in response: {[h for h in response.headers if h.startswith('Access-Control-')]}")

        return response
