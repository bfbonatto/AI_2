from random import random, randint, choices
import sys
from math import inf

def collide(one, two):
	x1,y1 = one
	x2,y2 = two
	x = abs(x1-x2)
	y = abs(y1-y2)
	return x == y or x == 0 or y == 0

def evaluate(individual):
	"""
	Recebe um indivíduo (lista de inteiros) e retorna o número de ataques
	entre rainhas na configuração especificada pelo indivíduo.
	Por exemplo, no individuo [2,2,4,8,1,6,3,4], o número de ataques é 9.

	:param individual:list
	:return:int numero de ataques entre rainhas no individuo recebido
	"""
	queens = [(i+1,q) for (i,q) in enumerate(individual)]
	collisions =[[collide(p1,p2) for p2 in queens[i+1:]] for (i,p1) in enumerate(queens)]
	return len([p for p in sum(collisions, []) if p])


def tournament(participants):
	"""
	Recebe uma lista com vários indivíduos e retorna o melhor deles, com relação
	ao numero de conflitos
	:param participants:list - lista de individuos
	:return:list melhor individuo da lista recebida
	"""
	return min(participants, key=evaluate)


def crossover(parent1, parent2, index):
	"""
	Realiza o crossover de um ponto: recebe dois indivíduos e o ponto de
	cruzamento (indice) a partir do qual os genes serão trocados. Retorna os
	dois indivíduos com o material genético trocado.
	Por exemplo, a chamada: crossover([2,4,7,4,8,5,5,2], [3,2,7,5,2,4,1,1], 3)
	deve retornar [2,4,7,5,2,4,1,1], [3,2,7,4,8,5,5,2].
	A ordem dos dois indivíduos retornados não é importante
	(o retorno [3,2,7,4,8,5,5,2], [2,4,7,5,2,4,1,1] também está correto).
	:param parent1:list
	:param parent2:list
	:param index:int
	:return:list,list
	"""
	p1 = parent1[:index] + parent2[index:]
	p2 = parent2[:index] + parent1[index:]
	return (p1,p2)


def mutate(individual, m):
	"""
	Recebe um indivíduo e a probabilidade de mutação (m).
	Caso random() < m, sorteia uma posição aleatória do indivíduo e
	coloca nela um número aleatório entre 1 e 8 (inclusive).
	:param individual:list
	:param m:int - probabilidade de mutacao
	:return:list - individuo apos mutacao (ou intacto, caso a prob. de mutacao nao seja satisfeita)
	"""
	i = individual.copy()
	if random() < m:
		i[randint(0,7)] = randint(1,8)
	return i


def run_ga(g, n, k, m, e):
	"""
	Executa o algoritmo genético e retorna o indivíduo com o menor número de ataques entre rainhas
	:param g:int - numero de gerações
	:param n:int - numero de individuos
	:param k:int - numero de participantes do torneio
	:param m:float - probabilidade de mutação (entre 0 e 1, inclusive)
	:param e:bool - se vai haver elitismo
	:return:list - melhor individuo encontrado
	"""
	population = [[ randint(1,8) for _ in range(8)] for _ in range(n)]
	for _ in range(g):
		new_pop = []
		if e:
			new_pop.append(min(population, key=evaluate))
		while len(new_pop) < n:
			parent1 = tournament(choices(population, k=k))
			parent2 = tournament(choices(population, k=k))
			n1,n2 = crossover(parent1, parent2, randint(0,7))
			new_pop.append(mutate(n1,m))
			new_pop.append(mutate(n2,m))
		population = new_pop
	return min(population, key=evaluate)


best = inf

for g in range(5,20):
	for n in range(10,30):
		for k in range(1,n):
			for m in [0,0.25,0.5,0.75,1]:
				ga = run_ga(g,n,k,m,True)
				ega = evaluate(ga)
				if ega < best:
					print(f"new best found with g={g} n={n} k={k} m={m} with value={ega}")
					best = ega
				if ega == 0:
					print(f"solution found with g={g} n={n} k={k} m={m}, solution={ga}")
