
from django import forms
from .models import DeliveryDetails

class DeliveryDetailsForm(forms.ModelForm):
    paypal_email = forms.EmailField(required=False)
    mobile_money_number = forms.CharField(max_length=15, required=False)

    class Meta:
        model = DeliveryDetails
        fields = ['location', 'phone_number', 'payment_method']
        widgets = {
            'payment_method': forms.RadioSelect,
        }

    def clean(self):
        cleaned_data = super().clean()
        payment_method = cleaned_data.get('payment_method')

        # Validate PayPal email if PayPal is chosen
        if payment_method == 'PayPal':
            paypal_email = cleaned_data.get('paypal_email')
            if not paypal_email:
                raise forms.ValidationError('PayPal email is required for PayPal payment method.')

        # Validate Mobile Money number if Mobile Money is chosen
        elif payment_method == 'MM':
            mobile_money_number = cleaned_data.get('mobile_money_number')
            if not mobile_money_number:
                raise forms.ValidationError('Mobile Money number is required for Mobile Money payment method.')

        return cleaned_data

