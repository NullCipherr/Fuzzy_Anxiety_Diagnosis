#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 14:59:09 2024

@author: zerocool
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Criação das variáveis de entrada
freq_cardiaca = ctrl.Antecedent(np.arange(60, 121, 1), 'frequencia_cardiaca')
preocupacao = ctrl.Antecedent(np.arange(0, 11, 1), 'nivel_preocupacao')
sono = ctrl.Antecedent(np.arange(0, 11, 1), 'qualidade_sono')
tensao = ctrl.Antecedent(np.arange(0, 11, 1), 'tensao_muscular')

# Criação da variável de saída
ansiedade = ctrl.Consequent(np.arange(0, 101, 1), 'nivel_ansiedade')

# Definição das funções de pertinência para frequência cardíaca
freq_cardiaca['normal'] = fuzz.trapmf(freq_cardiaca.universe, [60, 60, 70, 80])
freq_cardiaca['elevada'] = fuzz.trimf(freq_cardiaca.universe, [70, 85, 100])
freq_cardiaca['muito_elevada'] = fuzz.trapmf(freq_cardiaca.universe, [90, 100, 120, 120])

# Definição das funções de pertinência para nível de preocupação
preocupacao['baixo'] = fuzz.trimf(preocupacao.universe, [0, 0, 5])
preocupacao['moderado'] = fuzz.trimf(preocupacao.universe, [3, 5, 7])
preocupacao['alto'] = fuzz.trimf(preocupacao.universe, [5, 10, 10])

# Definição das funções de pertinência para qualidade do sono
sono['boa'] = fuzz.trimf(sono.universe, [7, 10, 10])
sono['regular'] = fuzz.trimf(sono.universe, [3, 5, 7])
sono['ruim'] = fuzz.trimf(sono.universe, [0, 0, 3])

# Definição das funções de pertinência para tensão muscular
tensao['relaxada'] = fuzz.trimf(tensao.universe, [0, 0, 4])
tensao['moderada'] = fuzz.trimf(tensao.universe, [3, 5, 7])
tensao['tensa'] = fuzz.trimf(tensao.universe, [6, 10, 10])

# Definição das funções de pertinência para nível de ansiedade
ansiedade['baixo'] = fuzz.trimf(ansiedade.universe, [0, 0, 40])
ansiedade['moderado'] = fuzz.trimf(ansiedade.universe, [30, 50, 70])
ansiedade['alto'] = fuzz.trimf(ansiedade.universe, [60, 100, 100])

# Definição das regras
regra1 = ctrl.Rule(freq_cardiaca['normal'] & preocupacao['baixo'] & sono['boa'] & tensao['relaxada'], ansiedade['baixo'])
regra2 = ctrl.Rule(freq_cardiaca['elevada'] & preocupacao['moderado'] & sono['regular'] & tensao['moderada'], ansiedade['moderado'])
regra3 = ctrl.Rule(freq_cardiaca['muito_elevada'] & preocupacao['alto'] & sono['ruim'] & tensao['tensa'], ansiedade['alto'])
regra4 = ctrl.Rule(freq_cardiaca['elevada'] | preocupacao['alto'] | sono['ruim'] | tensao['tensa'], ansiedade['moderado'])
regra5 = ctrl.Rule(freq_cardiaca['normal'] & preocupacao['baixo'] & (sono['boa'] | sono['regular']) & tensao['relaxada'], ansiedade['baixo'])

# Criação do sistema de controle
sistema_ctrl = ctrl.ControlSystem([regra1, regra2, regra3, regra4, regra5])

# Criação da simulação
simulacao = ctrl.ControlSystemSimulation(sistema_ctrl)

# Função para diagnóstico
def diagnostico_ansiedade(freq_card, nivel_preoc, qual_sono, tensao_musc):
    simulacao.input['frequencia_cardiaca'] = freq_card
    simulacao.input['nivel_preocupacao'] = nivel_preoc
    simulacao.input['qualidade_sono'] = qual_sono
    simulacao.input['tensao_muscular'] = tensao_musc
    
    simulacao.compute()
    
    nivel_ansiedade = simulacao.output['nivel_ansiedade']
    print(f"Nível de Ansiedade: {nivel_ansiedade:.2f}")
    
    if nivel_ansiedade < 30:
        return "Baixo nível de ansiedade"
    elif 30 <= nivel_ansiedade < 60:
        return "Nível moderado de ansiedade"
    else:
        return "Alto nível de ansiedade"

def entrada_manual():
    freq_card = float(input("Digite a frequência cardíaca (60-120 bpm): "))
    nivel_preoc = float(input("Digite o nível de preocupação (0-10): "))
    qual_sono = float(input("Digite a qualidade do sono (0-10, onde 10 é ótimo): "))
    tensao_musc = float(input("Digite o nível de tensão muscular (0-10): "))
    
    resultado = diagnostico_ansiedade(freq_card, nivel_preoc, qual_sono, tensao_musc)
    print(resultado)

def entrada_arquivo():
    nome_arquivo = input("Digite o nome do arquivo de entrada (incluindo .txt): ")
    try:
        with open(nome_arquivo, 'r') as arquivo:
            linhas = arquivo.readlines()
            for i, linha in enumerate(linhas, 1):
                dados = linha.strip().split(',')
                if len(dados) != 4:
                    print(f"Erro na linha {i}: formato inválido")
                    continue
                try:
                    freq_card, nivel_preoc, qual_sono, tensao_musc = map(float, dados)
                    print(f"\nCaso {i}:")
                    resultado = diagnostico_ansiedade(freq_card, nivel_preoc, qual_sono, tensao_musc)
                    print(resultado)
                except ValueError:
                    print(f"Erro na linha {i}: valores inválidos")
    except FileNotFoundError:
        print("Arquivo não encontrado.")

# Menu principal
while True:
    print("\nSistema de Diagnóstico de Ansiedade")
    print("1. Entrada manual")
    print("2. Carregar de arquivo")
    print("3. Sair")
    
    opcao = input("Escolha uma opção: ")
    
    if opcao == '1':
        entrada_manual()
    elif opcao == '2':
        entrada_arquivo()
    elif opcao == '3':
        print("Encerrando o programa.")
        break
    else:
        print("Opção inválida. Tente novamente.")
