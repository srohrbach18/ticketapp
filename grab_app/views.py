from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.validate(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect('/')
    else:
        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        ) 
        request.session['user_id'] = user.id
        request.session['greeting'] = user.first_name
        return redirect('/success')

def login(request):
    if request.method == "GET":
        return redirect('/')
    if not User.objects.authenticate(request.POST['email'], request.POST['password']):
        messages.error(request, 'Invalid Email/Password')
        return redirect('/')
    user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = user.id
    request.session['greeting'] = user.first_name
    return redirect('/success')

def logout(request):
    request.session.clear()
    return redirect('/')

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        context = {
            'all_games': Games.objects.all(),
            'this_user': User.objects.get(id=request.session['user_id'])
        }
        return render(request, 'main_page.html', context)

def new(request):
    return render(request, 'add_one.html')

def create_game(request):
    errors = Games.objects.game_validator(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/games/new')
    else:
        user = User.objects.get(id=request.session["user_id"])
        game = Games.objects.create(
            opp = request.POST['opp'],
            date = request.POST['date'],
            location = request.POST['location'],
            creator = user
        )
        return redirect('/success')

def show_one(request, game_id):
    print(Games.objects.get(id=game_id).joined_by.all())
    context = {
        'game': Games.objects.get(id=game_id),
        'this_user': User.objects.get(id=request.session['user_id']),
    }
    return render(request, "show_one.html", context)

def grab(request, game_id):
    user = User.objects.get(id=request.session["user_id"])
    game = Games.objects.get(id=game_id)
    user.joined_games.add(game)
    return redirect(f'/games/{game.id}')

def profile(request):
    context = {
        'this_user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, "profile.html", context)

def delete(request, game_id):
    to_delete = Games.objects.get(id=game_id)
    to_delete.delete()
    return redirect('/success')

def post_mess(request, game_id):
    game = Games.objects.get(id=game_id)
    user = User.objects.get(id=request.session["user_id"])
    user.joined_games.add(game)
    Wall_Message.objects.create(message=request.POST['mess'], poster=user, game_assc=game)
    return redirect(f'/games/{game.id}')

def post_comment(request, message_id):
    game = Games.objects.get(id=message_id)
    poster = User.objects.get(id=request.session['user_id'])
    message = Wall_Message.objects.get(id=message_id)
    Comment.objects.create(comment=request.POST['comment'], poster=poster, wall_message=message)
    return redirect(f'/games/{game.id}')

def add_like(request, message_id):
    liked_message = Wall_Message.objects.filter(id=message_id)
    user_liking = User.objects.get(id=request.session['user_id'])
    liked_message.user_likes.add(user_liking)
    return redirect('/success')

def delete_comment(request, message_id):
    destroyed = Wall_Message.objects.get(id=message_id)
    destroyed.delete()
    return redirect('/success')
