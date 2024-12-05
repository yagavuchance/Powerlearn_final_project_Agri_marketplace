from django import forms
from products.models import Product, Category

class ProductForm(forms.ModelForm):
    new_category = forms.CharField(
        max_length=100,
        required=False,
        label="New Category",
        help_text="Enter a new category if it doesn't exist.",
    )

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'stock', 'image']

    def save(self, commit=True):
        # If a new category is provided, create it
        new_category_name = self.cleaned_data.get('new_category')
        if new_category_name:
            category, created = Category.objects.get_or_create(name=new_category_name)
            self.instance.category = category

        return super().save(commit=commit)
