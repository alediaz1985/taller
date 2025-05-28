from django import forms

class ContactoForm(forms.Form):
    name = forms.CharField(max_length=100, label='Nombre Completo')
    email = forms.EmailField(label='Correo Electrónico')
    phone = forms.CharField(max_length=15, required=False, label='Teléfono')
    message = forms.CharField(widget=forms.Textarea, label='Mensaje')

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not phone.isdigit():
            raise forms.ValidationError("El teléfono solo debe contener números.")
        return phone
