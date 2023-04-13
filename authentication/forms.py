from django import forms


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        label="Current password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password = forms.CharField(
        label="New password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(
        label="Confirm password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
