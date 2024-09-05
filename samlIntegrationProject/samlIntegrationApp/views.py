# views.py

from django.shortcuts import render, redirect
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from samlIntegrationProject.saml_settings import SAML_SETTINGS
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def init_saml_auth(req):
    auth = OneLogin_Saml2_Auth(req,SAML_SETTINGS)
    return auth

@csrf_exempt
def prepare_django_request(request):
    # Django specific way of parsing the SAML request
    return {
        'http_host': request.META['HTTP_HOST'],
        'server_port': request.META['SERVER_PORT'],
        'script_name': request.META['PATH_INFO'],
        'get_data': request.GET.copy(),
        'post_data': request.POST.copy(),
        'https': 'on' if request.is_secure() else 'off',
    }

@csrf_exempt
def saml_acs(request):
    req = prepare_django_request(request)
    auth = init_saml_auth(req)
    auth.process_response()
    errors = auth.get_errors()
    if not errors:
        request.session['samlUserdata'] = auth.get_attributes()
        request.session['samlNameId'] = auth.get_nameid()
        # Redirect to a success page
        return render(request,'home.html')
    else:
        return render(request, 'error.html', {'errors': errors})

@csrf_exempt
def saml_login(request):
    print("entered")
    req = prepare_django_request(request)
    auth = init_saml_auth(req)
    return redirect(auth.login())


@csrf_exempt
def saml_logout(request):
    req = prepare_django_request(request)
    auth = init_saml_auth(req)
    logout_url = auth.logout(name_id=request.session.get('samlNameId'))
   
    if 'SAMLResponse' in request.GET: 
        auth.process_slo()
        if not auth.get_errors():
            request.session.flush() 
            return redirect('saml_login')  
        else:
            errors = auth.get_errors()
            return render(request, 'error.html', {'errors': errors})
   
    return redirect(logout_url)


