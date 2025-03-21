from rest_framework.response import Response


def create_cookie_response(
    key, 
    value, 
    message, 
    status_code, 
    access_token,
    is_profile_professional=False
    ):
    response = Response(
        {
            'message': message ,
            'access_token': access_token, 
            'is_profile_professional': is_profile_professional
        }, 
        status=status_code,
        
    )
    response.set_cookie(
        key=key,
        value=value,
        httponly=True,  # Prevent JavaScript from accessing the cookie
        secure=False,   # Set to True in production
        samesite='strict', # Prevent cross-site request forgery
        max_age=60 * 60 * 24 * 7,  # 7 days in seconds
    )
    return response

def delete_cookie_response(key, message, status_code):
    response = Response(
        {'message': message},
        status=status_code
    )
    response.delete_cookie("refresh_token")
    return response