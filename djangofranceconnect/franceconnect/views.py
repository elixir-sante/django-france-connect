# Import Django stuff
from django.shortcuts import render, redirect
from django.http import HttpResponse

# Import FC stuff
from .models import FranceConnectAuth

def index(request):
    return render(request, 'franceconnect/index.html')


def connect(request):
    # Prepare and return authorization URL
    fc = FranceConnectAuth()
    return redirect(fc.authorize())


def disconnect(request):
    # Getting token from session
    id_token = request.session['fc_id_token']
    fc = FranceConnectAuth()
    return redirect(fc.logout(id_token))


def callback_logout(request):
    # Doing your disconnect stuff
    print('You can logout your user here')

    # Cleat token from session
    del request.session['fc_id_token']
    return render(request, 'franceconnect/disconnect.html')


def callback_login(request):
    
    # Get minimal info for getting token
    code = request.GET.get('code', None)
    state = request.GET.get('state', None)

    if code is None:
        # Do something with this error
        return HttpResponse('ERROR')
    print("Authorize OK")

    # Get token
    fc = FranceConnectAuth()
    id_token = fc.token(code)
    print('Token OK')

    # Get userinfo
    userinfo = fc.userinfo('identite_pivot')
    print('Userinfo OK')

    # Doing your app stuff
    print('You can register user datas here')
    print('You can login your user here')

    # Resgister user token in session
    request.session['fc_id_token'] = id_token

    # Run your app
    return render(request, 'franceconnect/app.html', context = {'userinfo': userinfo})
