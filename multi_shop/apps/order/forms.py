from django import forms
from .models import Address, City, Province


class AddressForm(forms.ModelForm):
    user = forms.IntegerField(required=False)

    class Meta:
        model = Address
        fields = [
            "user",
            "recipient_name",
            "building_number",
            "unit",
            "street",
            "postal_code",
            "city",
            "province",
            "full_address",
        ]
        widgets = {
            "city": forms.Select(choices=(("reza", "ali"))),
            "province": forms.Select(),
            "recipient_name": forms.TextInput({"placeholder": "John Doe"}),
            "building_number": forms.TextInput({"placeholder": "123"}),
            "unit": forms.TextInput({"placeholder": "4B"}),
            "street": forms.TextInput({"placeholder": "Main St"}),
            "postal_code": forms.TextInput({"placeholder": "12345"}),
            "full_address": forms.Textarea(
                {"placeholder": "123 Main St, Apt 4B, New York, NY 12345"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["city"].queryset = City.objects.all()
        self.fields["province"].queryset = Province.objects.all()

        if self.fields["city"].queryset.exists():
            self.initial["city"] = self.fields["city"].queryset.first().id
        if self.fields["province"].queryset.exists():
            self.initial["province"] = self.fields["province"].queryset.first().id
