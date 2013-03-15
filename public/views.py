from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from public.forms import CreateRepositoryForm, LoginForm, CreateAccountForm
from django.contrib.auth.models import User

from core.models import Repository
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.http import HttpResponse
import json

class HttpJSONResponse(HttpResponse):
    def __init__(self, data):
        serialized = json.dumps(data)
        super(HttpJSONResponse, self).__init__(serialized, content_type="application/json")

def main(request):
    return render_to_response("public/main.dtml", {}, context_instance=RequestContext(request))

def create_account(request):
    if request.method == "POST":
        result = {
            "status" : "success",
            "messages" : []
        }
        
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            instance = form.save()            
        else:
            result["status"] = "failed"
            result["messages"] = form.errors

        return HttpJSONResponse(result)
    else:
        form = CreateAccountForm()
        
    subs = {
        "form" : form
    }        
    
    return render_to_response("public/create_account.dtml", subs, context_instance=RequestContext(request))
    

def login_view(request):
    if request.method == "POST":
        result = {
            'status' : 'success',
            'messages' : []
        }

        form = LoginForm(request.POST)
        
        if form.is_valid():               
            username_or_email = form.cleaned_data['username_or_email']            
            password = form.cleaned_data['password']
            user = authenticate(username=username_or_email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)                    
                else:
                    result['status'] = 'failed'
                    result['messages'] = [ "Your account has been disabled" ]
            else:
                # Return an 'invalid login' error message.
                result['status'] = 'failed'
                result['messages'] = [ "Invalid username and/or password" ]
        else:
            result['status'] = 'failed'
            result['messages'] = form.errors

        return HttpJSONResponse(result)                
    else:
        form = LoginForm()
        
    subs = {
        'form' : form
    }
    
    return render_to_response("public/login.dtml", subs, context_instance=RequestContext(request))

def logout_view(request):
    logout(request)
    return redirect("public_main")

@login_required    
def create_repository(request, username):
    if request.method == "POST":
        form = CreateRepositoryForm(request, request.POST, request.FILES)
        
        if form.is_valid():
            instance = form.save()
            return redirect("public_view_repository", kwargs={"repository_id" : instance.pk})
            
    else:
        form = CreateRepositoryForm(request)
        
    subs = {
        "form" : form
    }        
    return render_to_response("public/create_repository.dtml", subs, context_instance=RequestContext(request))
    
def view_repository(request, username, repository_id):
    repo = get_object_or_404(Repository, pk=repository_id)
    
    subs = {
        "repo" : repo
    }
    
    return render_to_response("public/view_repository.dtml", subs, context_instance=RequestContext(request))
    
def user_repositories(request, username):
    user = get_object_or_404(User, username=username)

    repositories = user.repositories.all()
    subs = {
        "repositories" : repositories,
        "owner" : user
    } 
    
    return render_to_response("public/user_repositories.dtml", subs, context_instance=RequestContext(request))

@login_required
def create_package(request):    
    if request.method == "POST":
        form = CreatePackageForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            return redirect("public_view_package", kwargs={"package_id" : instance.pk})
    else:
        form = CreatePackageForm()

    subs = {
        "form" : form
    }        
    return render_to_response("public/create_package.dtml", subs, context_instance=RequestContext(request))
    
def view_package(request, package_id):
    package = get_object_or_404(Package, pk=package_id)
    
    subs = {
        "package": package
    }
    
    return render_to_response("public/view_package.dtml", subs, context_instance=RequestContext(request))

