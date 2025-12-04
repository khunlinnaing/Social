from django import forms
from project.models import Post
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'video']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'What\'s happening in your world?', 'rows':3}),
            'image': forms.FileInput(attrs={'class': 'form-control d-none'}),
            'video': forms.FileInput(attrs={'class': 'form-control d-none'}), 
            }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        
    def clean_image(self):
        image = self.cleaned_data.get('image')

        if image:
            allowed_extensions = ['png', 'jpg', 'jpeg']
            ext = image.name.split('.')[-1].lower()
            if ext not in allowed_extensions:
                raise forms.ValidationError("Only PNG, JPG, and JPEG images are allowed.")
            if image.content_type not in ['image/png', 'image/jpg', 'image/jpeg', 'image/pjpeg']:
                raise forms.ValidationError("Invalid image format.")
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Image file must be under 5MB.")
        return image
    
    def clean_video(self):
        video = self.cleaned_data.get('video')

        if video:
            # Allowed video extensions
            allowed_extensions = ['mp4']
            ext = video.name.split('.')[-1].lower()
            if ext not in allowed_extensions:
                raise forms.ValidationError("Only MP4 videos are allowed.")
            if video.content_type not in ['video/mp4']:
                raise forms.ValidationError("Invalid video format.")
            if video.size > 50 * 1024 * 1024:
                raise forms.ValidationError("Video file must be under 50MB.")

        return video