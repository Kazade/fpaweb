from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from public.forms import CreateRepositoryForm
from django.contrib.auth.models import User

from core.models import Repository
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

def main(request):
    return render_to_response("public/main.dtml", {}, context_instance=RequestContext(request))

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("public_user_repositories", username=user.username)
            else:
                # Return a 'disabled account' error message
                pass
        else:
            # Return an 'invalid login' error message.
            pass
    else:
        return render_to_response("public/login.dtml", subs, request_context=RequestContext(request))

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
        "user" : user
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

