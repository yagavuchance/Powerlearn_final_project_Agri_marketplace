from django import forms

class PaymentForm(forms.Form):
    amount_paid = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label="Enter the total amount",
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )
