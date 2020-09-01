from django import forms
from .productModel import Product, Product_category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product

        fields = ['product_category_id', 'product_name', 'product_description', 'product_images', 'product_price', 'product_status',
                  'discount', 'rating',
                  ]
        widgets = {
            'product_category_id': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'product_name': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'product_description': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),

            'product_price': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'product_status': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'discount': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'rating': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
        }

class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model = Product_category

        fields = ['category_name', 'category_description', 'product_thumbnail'
                  ]
        widgets = {
            'category_name': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'category_description': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            # 'status': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
        }