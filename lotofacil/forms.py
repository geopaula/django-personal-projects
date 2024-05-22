from django import forms
from .models import LotofacilResult


class LotofacilForm(forms.Form):

    concurso = forms.IntegerField(
        label='Número do sorteio',
        help_text='Insira o número do sorteio que deseja verificar',
        widget=forms.TextInput(attrs={'placeholder': '0000',
                                      'class': 'form-control form-control-sm ',}),
    )

    numbers = forms.CharField(
        label='Números Jogados',
        help_text='Insira os números separados por espaço',
        widget=forms.Textarea(attrs={'rows': 1, 
                                     'cols': 1, 
                                     'placeholder': '1 2 3 4 5 6 7 8 9 10 11 12 16 14 15 16 17 18 19 20',
                                     'class': 'form-control form-control-sm',}), 
    )

    def clean_concurso(self):
        data = self.cleaned_data['concurso']
        concurso = data
        
        # verificando se o concurso existe no banco de dados
        if int(concurso) not in LotofacilResult.objects.values_list('concurso', flat=True):
            raise forms.ValidationError("Concurso não encontrado. Verifique a digitação e tente novamente.")
        
        return concurso
    


    def clean_numbers(self):
        # retirando as informações do dicionário do django 'cleaned_data' e atribuindo a uma variável
        data = self.cleaned_data['numbers']
        numbers = [int(n) for n in data.split() if n.isdigit()]

        
        if not all(1 <= n <= 25 for n in numbers):
            raise forms.ValidationError("Os números devem estar entre 1 e 25.")
        
        if not (15 <= len(numbers) <= 20):
            raise forms.ValidationError("Insira entre 15 e 20 números.")
        
        return numbers
    


