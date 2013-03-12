from django.shortcuts import render_to_response
from django.template import RequestContext
from public.forms import CreateRepositoryForm

from core.models import Repository

def main(request):
    return render_to_response("public/main.dtml", {}, context_instance=RequestContext(request))
    
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
    
def view_repository(request, repository_id):
    repo = get_object_or_404(Repository, pk=repository_id)
    
    subs = {
        "repo" : repo
    }
    
    return render_to_response("public/view_repository.dtml", subs, context_instance=RequestContext(request))
    
def user_repositories(request, username):
    repositories = Repository.objects.filter(owner__username=username).all()
    subs = {
        "repositories" : repositories
    } 
    
    return render_to_response("public/user_repositories.dtml", subs, context_instance=RequestContext(request))
    
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

