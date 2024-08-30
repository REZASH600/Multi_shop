from django import forms
from . import models
from django.core.exceptions import ValidationError


class CommentForm(forms.ModelForm):
    user = forms.IntegerField(required=False)
    product = forms.IntegerField(required=False)
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(),
        required=False,
    )
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(),
        required=False,
    )

    class Meta:
        model = models.Comment
        fields = ["user", "product", "message"]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        self.product = kwargs.pop("product", None)
        super().__init__(*args, **kwargs)

    def clean_first_name(self):
        
        first_name = self.cleaned_data.get("first_name")
        if self.request.user.first_name is None:
            if not first_name:
                raise ValidationError("please enter first name")
               

        return first_name

    def save(self, commit=True):

        obj = super().save(commit=False)
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")

        if commit:

            if self.request and self.request.user.is_authenticated:

                user = self.request.user

                if first_name:
                    user.first_name = first_name

                if last_name:
                    user.last_name = last_name

                user.save()
                obj.user = self.request.user

            if self.product:
                obj.product = self.product

            obj.save()

        return obj
