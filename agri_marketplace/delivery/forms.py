from django import forms
from .models import DeliveryDetails

class DeliveryDetailsForm(forms.ModelForm):
    paypal_email = forms.EmailField(required=False, label="PayPal Email")
    mobile_money_number = forms.CharField(max_length=15, required=False, label="Mobile Money Number")
    card_number = forms.CharField(max_length=16, required=False, label="Card Number")
    card_expiry = forms.CharField(max_length=5, required=False, label="Expiry Date (MM/YY)")
    card_cvc = forms.CharField(max_length=4, required=False, label="CVC Code")

    class Meta:
        model = DeliveryDetails
        fields = ['location', 'phone_number', 'payment_method']
        widgets = {
            'payment_method': forms.RadioSelect,
        }

    def clean(self):
        cleaned_data = super().clean()
        payment_method = cleaned_data.get('payment_method')

        if payment_method == 'PayPal':
            paypal_email = cleaned_data.get('paypal_email')
            if not paypal_email:
                raise forms.ValidationError('PayPal email is required for PayPal payment method.')

        elif payment_method == 'MM':
            mobile_money_number = cleaned_data.get('mobile_money_number')
            if not mobile_money_number:
                raise forms.ValidationError('Mobile Money number is required for Mobile Money payment method.')

        elif payment_method == 'Debit':
            card_number = cleaned_data.get('card_number')
            card_expiry = cleaned_data.get('card_expiry')
            card_cvc = cleaned_data.get('card_cvc')
            if not (card_number and card_expiry and card_cvc):
                raise forms.ValidationError('All card details are required for Debit Card payment.')

        return cleaned_data
