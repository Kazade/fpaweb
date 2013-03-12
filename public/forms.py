from core.models import Repository

from django import forms

class CreateRepositoryForm(forms.ModelForm):
    class Meta:
        model = Repository
        
    def __init__(self, request, *args, **kwargs):
        self.request = request        
        super(CreateRepositoryForm, self).__init__(*args, **kwargs)        
        