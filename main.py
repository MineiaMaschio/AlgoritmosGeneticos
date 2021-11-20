#Algoritmos genéticos - Problema do caixeiro viajante
#Equipe: Fábio Franz, Minéia Maschio e Paulo Ricardo Medeiros Gonçalves

from random import random
from random import randint
from numpy.random import choice
import numpy as np
import math
import random

#Definições
QNTD_CIDADES = 20
POPULACAO = 20
GERACOES = 10000
TAXA_MUTACAO = 0.05

class Cidade():
    def __init__(self, id):
        self.id = id
        self.pontoX = random.uniform(0, 1)
        self.pontoY = random.uniform(0, 1)

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
        return populacao

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
        return fitness

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

    def selecionarPais(self, listaFitnessPopulacao):
        resultadoFitness = []

        # Pega apenas o valor fitness
        for i in listaFitnessPopulacao:
            resultadoFitness.append(i[0])

        #Soma fitness e calcular probabilidade
        somaFitness = sum(resultadoFitness)
        probabilidade = [f/somaFitness for f in resultadoFitness]

        #Gerar lista e escolher primeiro valor
        resultado = choice(resultadoFitness, size=POPULACAO, p=probabilidade)
        primeiraEscolha = resultado[:1]

        #Buscando na lista novamente para retornar com a população
        for i in listaFitnessPopulacao:
            if i[0] in primeiraEscolha:
                pai = i[1]
        return pai

    def crossover(self, populacao, cidades):
        novaPopulacao = []

        listaOrdenada = self.ordenarPopulacao(populacao, cidades)
        for i in range(0, self.tamanhoPopulacao,2):

            #Selecionar pais
            genes1 = self.selecionarPais(listaOrdenada)
            genes2 = self.selecionarPais(listaOrdenada)

            #Selecione gene a ser alterado aleatoriamente
            selecionaGene = randint(0, len(genes1) - 1)

            #Trocar genes
            tmp = genes1[selecionaGene]
            genes1[selecionaGene] = genes2[selecionaGene]
            genes2[selecionaGene] = tmp

            genesTrocados = []
            genesTrocados.append(selecionaGene)
            while True:
                #Verificar se há genes duplicados
                geneDuplicado = self.genesDuplicados(genes1, genesTrocados)
                if(geneDuplicado == -1):
                    break

                #Trocar genes
                tmp = genes1[geneDuplicado]
                genes1[geneDuplicado] = genes2[geneDuplicado]
                genes2[geneDuplicado] = tmp
                genesTrocados.append(geneDuplicado)

            #Adicionar a população
            novaPopulacao.append(self.mutacao(genes1))
            novaPopulacao.append(self.mutacao(genes2))

        #Ordenar população em função da aptidão
        filhosOrdenados = self.ordenarPopulacao(novaPopulacao, cidades)
        return filhosOrdenados

    def genesDuplicados(self, genes, genesTrocados):
        for gene in range(len(genes)):
            if gene in genesTrocados:
                continue
            if len([g for g in genes if g == genes[gene]]) > 1:
                return gene

        return -1

    def mutacao(self, filho):
        taxaMutacao = random.random()
        if taxaMutacao < TAXA_MUTACAO:
            indice1 = randint(0, (self.quantidade - 1))
            indice2 = randint(0, self.quantidade - 1)
            tmp = filho[indice1]
            tmp2 = filho[indice2]
            filho[indice1] = tmp2
            filho[indice2] = tmp
        return filho

class AlgoritmoGenetico:
    def __init__(self):
        self.tamanhoPopulacao = POPULACAO
        self.qntdCidades = QNTD_CIDADES
        self.geracoes = GERACOES
        self.taxaMutacao = TAXA_MUTACAO
        self.melhores = []

    def resolver(self):
        #Criar cidades e gerar distancias
        cidades = Cidades()
        cidades.criarCidades()
        cidades.gerarDistancias()

        #Criar população
        individuos = Individuos()
        populacao = individuos.gerarCromossomos()

        #Crossover
        pop = individuos.crossover(populacao, cidades.distancias)

        #Realizar for em função da quantidade de gerações
        for i in range(self.geracoes):
            novaPopulacao = []

            #Adicionar nova população
            for j in range(self.tamanhoPopulacao):
                novaPopulacao.append(pop[j][1])

            #Realizar crossover
            filhos = individuos.crossover(novaPopulacao, cidades.distancias)

            #Adicionar na lista sempre o melhor resultado de cada geração
            melhor = filhos[0]
            self.melhores.append(melhor)

            #Adicionar nova população
            pop = filhos
        return self.melhores


if __name__ == '__main__':
    ag = AlgoritmoGenetico()
    teste = ag.resolver()
    teste.sort()
    print("Tamanho da população = ", POPULACAO)
    print("Taxa de mutação = ", TAXA_MUTACAO)
    print("Número de cidades = ", QNTD_CIDADES)
    print("Melhor custo = ", teste[0][0])
    print("Melhor solução = ", teste[0][1])
