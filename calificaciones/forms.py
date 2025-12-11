import re

from django import forms
from .models import Emisor, FactorTributario, Calificacion

class EmisorForm(forms.ModelForm):
    def clean_rut(self):
        rut = (self.cleaned_data.get('rut') or '').strip().upper()
        match = re.match(r'^\d{1,3}(?:\.?\d{3})*-([0-9K])$', rut)
        if not match:
            raise forms.ValidationError('Formato RUT inválido. Usa 12.345.678-9 y el DV solo puede ser 0-9 o K.')
        dv = match.group(1)
        if not (dv.isdigit() or dv == 'K'):
            raise forms.ValidationError('El dígito verificador solo puede ser 0-9 o K.')
        return rut

    class Meta:
        model = Emisor
        # Ajustado a tus campos reales: 'nombre' y 'direccion'
        fields = ['rut', 'nombre', 'direccion', 'activo']
        widgets = {
            'rut': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 12.345.678-9',
                'pattern': r'\d{1,3}(?:\.?\d{3})*-[0-9Kk]',
                'title': 'Formato RUT: 12.345.678-9 (DV 0-9 o K)',
                'inputmode': 'text',
                'autocomplete': 'off',
            }),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class FactorForm(forms.ModelForm):
    class Meta:
        model = FactorTributario
        # Ajustado a tus campos reales: 'codigo' y 'descripcion'
        fields = ['codigo', 'descripcion']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CalificacionForm(forms.ModelForm):
    class Meta:
        model = Calificacion
        fields = ['emisor', 'factor', 'comentario']
        widgets = {
            'emisor': forms.Select(attrs={'class': 'form-control select2'}),
            'factor': forms.Select(attrs={'class': 'form-control'}),
            'comentario': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class CargaMasivaForm(forms.Form):
    """Formulario para cargar calificaciones desde Excel o CSV"""
    archivo = forms.FileField(
        label='Archivo (.xlsx, .xls o .csv)',
        help_text='El archivo debe tener columnas: RUT, Código Factor, Comentario (Máximo 10 MB)',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.xlsx,.xls,.csv',
        })
    )
    
    def clean_archivo(self):
        archivo = self.cleaned_data.get('archivo')
        if archivo:
            # Tamaño máximo: 10 MB
            max_size = 10 * 1024 * 1024  # 10 MB en bytes
            if archivo.size > max_size:
                raise forms.ValidationError(
                    f'El archivo es demasiado grande ({archivo.size / (1024*1024):.2f} MB). '
                    f'El tamaño máximo permitido es 10 MB.'
                )
        return archivo