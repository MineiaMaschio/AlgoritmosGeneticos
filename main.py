#Algoritmos genéticos - Problema do caixeiro viajante
#Equipe: Fábio Franz, Minéia Maschio e Paulo Ricardo Medeiros Gonçalves

from random import random
from random import randint
import numpy as np
import math

#Definições
QNTD_CIDADES = 20
POPULACAO = 20
GERACOES = 10000
TAXA_MUTACAO = 0.05

class Cidade():
    def __init__(self, id):
        self.id = id
        self.pontoX = round(random() * 100)
        self.pontoY = round(random() * 100)

class Cidades():
    def __init__(self):
        self.quantidade = QNTD_CIDADES
        self.cidades = []
        self.distancias = []

    def criarCidades(self):
        for i in range(self.quantidade):
            cidade = Cidade(i)
            self.cidades.append(cidade)

    def gerarDistancias(self):
        qtd = self.quantidade
        distancias = np.zeros((qtd, qtd))
        for i in range(0, qtd):
            for j in range(0, qtd):
                distancias[i][j] = math.sqrt(((self.cidades[i].pontoX - self.cidades[j].pontoX) ** 2) + ((self.cidades[i].pontoY - self.cidades[j].pontoY) ** 2))
        self.distancias = distancias
        return distancias

class Individuos():
    def __init__(self):
        self.tamanhoPopulacao = POPULACAO
        self.quantidade = QNTD_CIDADES

    def gerarCromossomos(self):
        cromossomos = []
        populacao = []
        i = 1
        for i in range(self.tamanhoPopulacao):
            while len(cromossomos) != self.quantidade:
                j = randint(1, self.quantidade)
                if j not in cromossomos:
                    cromossomos.append(j)
            populacao.append(cromossomos)
            cromossomos = []
        self.populacao = populacao
        return self.populacao

    def fitness(self, populacao, distanciasCidades):
        fitness = []
        for i in range(self.tamanhoPopulacao):
            pop = []
            distancia = 0
            x = 0
            y = 0
            pop = populacao[i]
            for j in range(self.quantidade-1):
                x = pop[j]
                if(j < self.quantidade):
                    y = pop[j+1]
                else:
                    y = -1
                distancia += distanciasCidades[x-1][y-1]
            fitness.append(distancia)
        self.fitness = fitness
        return self.fitness

    def ordenarPopulacao(self, populucao, distanciaCidades):
        #Ordena populacao por função de aptidão
        lista = []
        if (len(populucao) == 0):
            populucao = self.gerarCromossomos()
        fitness = self.fitness(populucao, distanciaCidades)
        lista = list(zip(fitness, populucao))
        lista_ordenada = []
        lista_ordenada = sorted(lista, reverse=False)
        self.lista_ordenada = lista_ordenada
        return self.lista_ordenada

if __name__ == '__main__':
    cidades = Cidades()
    cidades.criarCidades()
    cidades.gerarDistancias()
    pop = Individuos()
    lista = pop.gerarCromossomos()
    lista2 = pop.ordenarPopulacao(lista, cidades.distancias)
    for x in lista2:
        print(x)