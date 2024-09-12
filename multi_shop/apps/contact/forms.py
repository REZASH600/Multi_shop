from django import forms


class ContactForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput({"placeholder": "Email"}), required=False
    )
    subject = forms.CharField(
        max_length=50, widget=forms.TextInput({"placeholder": "Subject"})
    )

    message = forms.CharField(
        widget=forms.Textarea({"placeholder": "Message", "rows": 8})
    )
