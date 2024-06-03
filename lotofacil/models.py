from django.db import models
import uuid

# Create your models here.

class LotofacilResult(models.Model):
    concurso = models.IntegerField(unique=True)
    data_sorteio = models.DateField()
    bola1 = models.IntegerField()
    bola2 = models.IntegerField()
    bola3 = models.IntegerField()
    bola4 = models.IntegerField()
    bola5 = models.IntegerField()
    bola6 = models.IntegerField()
    bola7 = models.IntegerField()
    bola8 = models.IntegerField()
    bola9 = models.IntegerField()
    bola10 = models.IntegerField()
    bola11 = models.IntegerField()
    bola12 = models.IntegerField()
    bola13 = models.IntegerField()
    bola14 = models.IntegerField()
    bola15 = models.IntegerField()
    ganhadores_15_acertos = models.IntegerField()
    rateio_15_acertos = models.CharField(max_length=20)
    ganhadores_14_acertos = models.IntegerField()
    rateio_14_acertos = models.CharField(max_length=20)
    ganhadores_13_acertos = models.IntegerField()
    rateio_13_acertos = models.CharField(max_length=20)
    ganhadores_12_acertos = models.IntegerField()
    rateio_12_acertos = models.CharField(max_length=20)
    ganhadores_11_acertos = models.IntegerField()
    rateio_11_acertos = models.CharField(max_length=20)
    acumulado_15_acertos = models.CharField(max_length=20)
    arrecadacao_total = models.CharField(max_length=20)
    estimativa_premio = models.CharField(max_length=20)
    acumulado_especial_independencia = models.CharField(max_length=20)
    observacao = models.TextField()

    def __str__(self):
        return f"Concurso {self.concurso} - {self.data_sorteio}"
    

class UserPicks(models.Model):
    play_number = models.IntegerField()
    concurso = models.IntegerField()
    number = models.IntegerField()
    

    