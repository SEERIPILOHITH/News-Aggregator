from django.shortcuts import render,redirect
from .forms import preference, customUserCreationForm
from .models import Article,UserProfile,Bookmark
from django.contrib.auth.models import User
import requests
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
# Create your views here.
def home_view(request):
    return render(request,"home.html")

def base_view(request):
    return(request,"base.html")

def login_view(request):
    if request.method =="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"invalid")
    return render(request,'login.html')

def logout_view(request):
    logout(request)
    messages.success(request,'you have been loggedout successfully')
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        form= customUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            UserProfile.objects.create(user=user)
            return redirect('login')
    else:
        form= customUserCreationForm()
        return render(request,"register.html",{'form':form})
 

def preference_view(request):
    if request.method == 'POST':
        form = preference(request.POST)
        if form.is_valid():
            # Check if the user already has a profile
            try:
                user_profile = UserProfile.objects.get(user=request.user)
                user_profile.topics = form.cleaned_data['topics']  # Update the topics
                user_profile.save()  # Save the updated UserProfile
            except UserProfile.DoesNotExist:
                # If no profile exists, create a new one
                user_profile = UserProfile(user=request.user, topics=form.cleaned_data['topics'])
                user_profile.save()
            return redirect('dashboard')  # Redirect after saving
    else:
        # If GET request, pre-fill the form with existing data if profile exists
        user_profile = UserProfile.objects.filter(user=request.user).first()
        form = preference(instance=user_profile)

    return render(request, "preferences.html", {'form': form})

def dashboard_view(request):
    user = request.user
    # Safely retrieve topics from UserProfile and split them into a list
    topics = user.userprofile.topics.split(',') if user.userprofile.topics else []
    
    news_list = []
    
    for topic in topics:
        # Construct the URL dynamically using the topic
        url = f"https://newsapi.org/v2/everything?q={topic.strip()}&apiKey=362dc96592214653a444a0253e05429b"
        
        try:
            response = requests.get(url).json()
            articles = response.get('articles', [])
            
            for article in articles:
                news_list.append({
                    'title': article.get('title', 'No title available'),  # Default value if missing
                    'description': article.get('description', 'No description available'),  # Default value if missing
                    'url': article.get('url', '#'),  # Default value if missing
                    'published_at': article.get('published_at', 'No date available')  # Default value if missing
                })
        except requests.exceptions.RequestException as e:
            print(f"Error fetching news for {topic}: {e}")
            # Optionally, you can add a placeholder or log the error properly
    
    return render(request, "dashboard.html", {"news_list": news_list})
    
def bookmark_view(request):
    bookmarks = Bookmark.objects.filter(user=request.user)
    return render(request,"news/bookmark.html",{'bookmarks':bookmarks})
def add_bookmark(request,article_id):
    article = Article.objects.get(id= article_id)
    Bookmark.objects.create(user=request.user,article= article)
    return redirect('bookmark.html')


def profile_view(request):
    if User.is_authenticated():
        
        users = UserProfile.objects.all()
    
    template= loader.get_template("profile.html")
    context={
        'users':users,
    }
    return HttpResponse(template.render(context,request))