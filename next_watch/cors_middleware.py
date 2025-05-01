class CustomCorsMiddleware:
    """
    Custom middleware to ensure CORS headers are properly set for all responses,
    especially for preflight requests.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Process the request and get the response
        response = self.get_response(request)
        
        # Check if this is a CORS preflight request (OPTIONS)
        if request.method == 'OPTIONS' and 'HTTP_ORIGIN' in request.META:
            # Ensure the response has the necessary CORS headers
            if 'Access-Control-Allow-Origin' not in response:
                # Get the origin from the request
                origin = request.META.get('HTTP_ORIGIN')
                # Set the CORS headers
                response['Access-Control-Allow-Origin'] = origin
                response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
                response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
                response['Access-Control-Allow-Credentials'] = 'true'
                response['Access-Control-Max-Age'] = '86400'  # 24 hours
                
            # Log for debugging
            print(f"Preflight request from origin: {request.META.get('HTTP_ORIGIN')}")
            print(f"CORS headers in preflight response: {[h for h in response.headers if h.startswith('Access-Control-')]}")
                
        return response
