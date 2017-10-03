from django import forms
from django.contrib.auth.models import User

import django_filters


class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(name='username', lookup_expr='icontains',
                                         widget=forms.TextInput(attrs={'placeholder': 'username'}))

    class Meta:
        model = User
        fields = ['username', ]