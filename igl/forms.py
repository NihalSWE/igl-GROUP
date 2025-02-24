from django import forms
from .models import *

class GalleryAlbumDetailsForm(forms.ModelForm):
    album = forms.ModelChoiceField(
        queryset=Gallery_Album.objects.all(),
        empty_label="Select an Album",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Gallery_AlbumDetails
        fields = ['album', 'image']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class BODForm(forms.ModelForm):
    class Meta:
        model = BOD
        fields = ['name', 'role', 'image', 'bio', 'portfolio_link', 'pdf']
# Form for Staff
class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['name', 'position', 'image', 'bio', 'portfolio_link', 'pdf']