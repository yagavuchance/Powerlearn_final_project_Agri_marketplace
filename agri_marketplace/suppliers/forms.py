from django import forms
from products.models import Product, Category

class ProductForm(forms.ModelForm):
    new_category = forms.CharField(
        max_length=100,
        required=True,  # Make it mandatory
        label="Category",
        help_text="Enter the category name for the product.",
    )

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'image']  # Removed 'category' from fields

    def clean_new_category(self):
        new_category_name = self.cleaned_data.get('new_category')
        if not new_category_name.strip():
            raise forms.ValidationError("Category name cannot be blank.")
        return new_category_name

    def save(self, commit=True):
        # Always create or retrieve the category from the provided new_category field
        new_category_name = self.cleaned_data.get('new_category')
        category, created = Category.objects.get_or_create(name=new_category_name)
        self.instance.category = category  # Assign the category to the product instance

        return super().save(commit=commit)
