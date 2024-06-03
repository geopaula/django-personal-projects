from django.shortcuts import render, redirect
import pandas as pd
import requests
from datetime import date
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .models import LotofacilResult
from .models import UserPicks
from .forms import LotofacilForm
import uuid



def lotofacil_view(request):
    page_title = 'Lotofácil'
    context = {'title': page_title}


    # buscar o último concurso para exibir na tela
    latest_result = LotofacilResult.objects.order_by('-concurso').first()
    context['latest_result'] = latest_result


    # verifica se o usuário acionou o botão 'atualizar resultados' e atualiza a tela
    if request.method == 'POST' and 'update' in request.POST:
        message = update_results()
        context['update_message'] = message
        return redirect('lotofacil')


    # processando o formulário 'verify'
    if request.method == 'POST' and 'verify' in request.POST:
        form = LotofacilForm(request.POST)

        if form.is_valid():

            # filtrando apenas o concurso escolhido pelo usuário
            chosen_concurso = LotofacilResult.objects.filter(concurso=form.cleaned_data['concurso']).first()
            
            save_concurso =  form.cleaned_data['concurso']

             # atribuindo os números digitados a uma variável e dividindo em uma lista
            user_chosen_numbers = form.cleaned_data['numbers']

            # chamando a função para salvar os números digitados pelo usuário
            save_user_picks(save_concurso, user_chosen_numbers)

            winning_numbers = [
                chosen_concurso.bola1, chosen_concurso.bola2, chosen_concurso.bola3, chosen_concurso.bola4,
                chosen_concurso.bola5, chosen_concurso.bola6, chosen_concurso.bola7, chosen_concurso.bola8,
                chosen_concurso.bola9, chosen_concurso.bola10, chosen_concurso.bola11, chosen_concurso.bola12,
                chosen_concurso.bola13, chosen_concurso.bola14, chosen_concurso.bola15
            ]

            # comparação números escolhidos x números vencedores
            matched_nums = set(user_chosen_numbers).intersection(winning_numbers)

            context['matched_nums'] = matched_nums
            context['amount_matched_nums'] = len(matched_nums)
            context['chosen_concurso'] = chosen_concurso

    else:
        form = LotofacilForm()

    context['form'] = form
    
    return render(request, 'lotofacil.html', context)


# função para guardar no banco de dados os números digitados pelo usuário 
def save_user_picks(save_concurso, user_chosen_numbers):
    
    i = 0
    if UserPicks.objects.filter(play_number = i).exists():
        i += 1

    for selected_number in user_chosen_numbers:
        UserPicks.objects.create(
            play_number = i,
            concurso = save_concurso,
            number = selected_number,
        )
       
       
        
                





# função para baixar os últimos resultados do site da Caixa
def update_results():  
    # url do excel com todos os resultados da lotofácil
    url = "https://servicebus2.caixa.gov.br/portaldeloterias/api/resultados/download?modalidade=Lotof%C3%A1cil"

    # atribuindo o file system storage do django a uma variável para conseguir guardar arquivos baixados na pasta MEDIA
    fss = FileSystemStorage(location=settings.MEDIA_ROOT)

    # especificando um nome para o arquivo excel baixado
    file_name = f"lotofacil_results_{date.today()}.xlsx"

    # juntado o MEDIA_ROOT das configurações com o nome do arquivo
    save_path = fss.path(f"lotofacil_results/{file_name}")

    # pegando o arquivo excel da url
    response = requests.get(url)
    
    # verificando a resposta da url
    if response.status_code == 200:
        # cria o arquivo, abre ele, escreve o conteúdo da requisição dentro, fecha o arquivo
        with open(save_path, 'wb') as file:
            file.write(response.content)
        
        # converte o arquivo excel em um data frame do pandas
        df = pd.read_excel(save_path, engine='openpyxl')

        # pegando o último concurso registrado no banco de dados
        last_concurso = LotofacilResult.objects.order_by('-concurso').first()

        # número do último concurso registrado no banco de dados
        last_concurso_number = last_concurso.concurso if last_concurso else 0

        # filtrar apenas os novos concursos
        new_data = df[df['Concurso'] > last_concurso_number]

         # iterar sobre as linhas do data frame filtrado e salvar no banco de dados
        for index, row in new_data.iterrows():
            LotofacilResult.objects.create(
                concurso=row['Concurso'],
                data_sorteio=pd.to_datetime(row['Data Sorteio'], format='%d/%m/%Y').date(),
                bola1=row['Bola1'],
                bola2=row['Bola2'],
                bola3=row['Bola3'],
                bola4=row['Bola4'],
                bola5=row['Bola5'],
                bola6=row['Bola6'],
                bola7=row['Bola7'],
                bola8=row['Bola8'],
                bola9=row['Bola9'],
                bola10=row['Bola10'],
                bola11=row['Bola11'],
                bola12=row['Bola12'],
                bola13=row['Bola13'],
                bola14=row['Bola14'],
                bola15=row['Bola15'],
                ganhadores_15_acertos=row['Ganhadores 15 acertos'],
                rateio_15_acertos=row['Rateio 15 acertos'],
                ganhadores_14_acertos=row['Ganhadores 14 acertos'],
                rateio_14_acertos=row['Rateio 14 acertos'],
                ganhadores_13_acertos=row['Ganhadores 13 acertos'],
                rateio_13_acertos=row['Rateio 13 acertos'],
                ganhadores_12_acertos=row['Ganhadores 12 acertos'],
                rateio_12_acertos=row['Rateio 12 acertos'],
                ganhadores_11_acertos=row['Ganhadores 11 acertos'],
                rateio_11_acertos=row['Rateio 11 acertos'],
                acumulado_15_acertos=row['Acumulado 15 acertos'],
                arrecadacao_total=row['Arrecadacao Total'],
                estimativa_premio=row['Estimativa Prêmio'],
                acumulado_especial_independencia=row['Acumulado sorteio especial Lotofácil da Independência'],
                observacao=row['Observação']
            )
        
        print(f"arquivo baixado e salvo em: {save_path}")
        print("dados carregados com sucesso no banco de dados!")
    else:
        print(f"download falhou. código de erro: {response.status_code}")
    
    return


