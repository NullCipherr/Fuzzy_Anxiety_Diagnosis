#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 14:59:09 2024

@author: nullcipherr
"""

import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class DiagnosticoAnsiedadeFuzzy:
  """
    Classe para realizar diagnóstico de ansiedade utilizando lógica fuzzy.

    Esta classe implementa um sistema de inferência fuzzy para avaliar o nível de ansiedade
    com base em quatro parâmetros: frequência cardíaca, nível de preocupação, qualidade do sono
    e tensão muscular.

    Attributes:
        freq_cardiaca (Antecedent): Variável fuzzy para frequência cardíaca.
        preocupacao (Antecedent): Variável fuzzy para nível de preocupação.
        sono (Antecedent): Variável fuzzy para qualidade do sono.
        tensao (Antecedent): Variável fuzzy para tensão muscular.
        ansiedade (Consequent): Variável fuzzy para nível de ansiedade (resultado).
        sistema_ctrl (ControlSystem): Sistema de controle fuzzy.
        simulacao (ControlSystemSimulation): Simulação do sistema de controle fuzzy.
  """


  def __init__(self):
    """
    Inicializa o sistema de diagnóstico de ansiedade fuzzy.

    Cria as variáveis fuzzy, define suas funções de pertinência,
    estabelece as regras fuzzy e configura o sistema de controle.
    """
    # Criação das variáveis fuzzy (antecedentes e consequente)
    self.freq_cardiaca = ctrl.Antecedent(np.arange(60, 121, 1), 'frequencia_cardiaca')
    self.preocupacao = ctrl.Antecedent(np.arange(0, 11, 1), 'nivel_preocupacao')
    self.sono = ctrl.Antecedent(np.arange(0, 11, 1), 'qualidade_sono')
    self.tensao = ctrl.Antecedent(np.arange(0, 11, 1), 'tensao_muscular')
    self.ansiedade = ctrl.Consequent(np.arange(0, 101, 1), 'nivel_ansiedade')

    # Configuração das funções de pertinência e regras fuzzy
    self.setup_fuzzy_variables()
    self.setup_fuzzy_rules()

    # Criação do sistema de controle e simulação
    self.sistema_ctrl = ctrl.ControlSystem(self.regras)
    self.simulacao = ctrl.ControlSystemSimulation(self.sistema_ctrl)

  def setup_fuzzy_variables(self):
    """
      Define as funções de pertinência para cada variável fuzzy.

      Utiliza diferentes tipos de funções de pertinência (trapezoidal e triangular)
      para representar os conjuntos fuzzy de cada variável.
    """
    # Definição das funções de pertinência para frequência cardíaca
    self.freq_cardiaca['normal'] = fuzz.trapmf(self.freq_cardiaca.universe, [60, 60, 70, 80])
    self.freq_cardiaca['elevada'] = fuzz.trimf(self.freq_cardiaca.universe, [70, 85, 100])
    self.freq_cardiaca['muito_elevada'] = fuzz.trapmf(self.freq_cardiaca.universe, [90, 100, 120, 120])

    # Definição das funções de pertinência para nível de preocupação
    self.preocupacao['baixo'] = fuzz.trimf(self.preocupacao.universe, [0, 0, 5])
    self.preocupacao['moderado'] = fuzz.trimf(self.preocupacao.universe, [3, 5, 7])
    self.preocupacao['alto'] = fuzz.trimf(self.preocupacao.universe, [5, 10, 10])

    # Definição das funções de pertinência para qualidade do sono
    self.sono['boa'] = fuzz.trimf(self.sono.universe, [7, 10, 10])
    self.sono['regular'] = fuzz.trimf(self.sono.universe, [3, 5, 7])
    self.sono['ruim'] = fuzz.trimf(self.sono.universe, [0, 0, 3])

    # Definição das funções de pertinência para tensão muscular
    self.tensao['relaxada'] = fuzz.trimf(self.tensao.universe, [0, 0, 4])
    self.tensao['moderada'] = fuzz.trimf(self.tensao.universe, [3, 5, 7])
    self.tensao['tensa'] = fuzz.trimf(self.tensao.universe, [6, 10, 10])

    # Definição das funções de pertinência para nível de ansiedade
    self.ansiedade['baixo'] = fuzz.trimf(self.ansiedade.universe, [0, 0, 40])
    self.ansiedade['moderado'] = fuzz.trimf(self.ansiedade.universe, [30, 50, 70])
    self.ansiedade['alto'] = fuzz.trimf(self.ansiedade.universe, [60, 100, 100])


  def setup_fuzzy_rules(self):
    """
      Define as regras do sistema fuzzy.

      Estabelece um conjunto de regras que relacionam as variáveis de entrada
      (antecedentes) com a variável de saída (consequente), formando a base de
      conhecimento do sistema fuzzy.
    """

    self.regras = [
      # Regra 1: Frequência cardíaca normal, baixo nível de preocupação, boa qualidade do sono, tensão muscular relaxada
      # Resulta em baixo nível de ansiedade
      ctrl.Rule(self.freq_cardiaca['normal'] & self.preocupacao['baixo'] & self.sono['boa'] & self.tensao['relaxada'], self.ansiedade['baixo']),

      # Regra 2: Frequência cardíaca elevada, moderada preocupação, sono regular, tensão muscular moderada
      # Resulta em nível moderado de ansiedade
      ctrl.Rule(self.freq_cardiaca['elevada'] & self.preocupacao['moderado'] & self.sono['regular'] & self.tensao['moderada'], self.ansiedade['moderado']),

      # Regra 3: Frequência cardíaca muito elevada, alto nível de preocupação, sono ruim, tensão muscular tensa
      # Resulta em alto nível de ansiedade
      ctrl.Rule(self.freq_cardiaca['muito_elevada'] & self.preocupacao['alto'] & self.sono['ruim'] & self.tensao['tensa'], self.ansiedade['alto']),

      # Regra 4: Qualquer um dos antecedentes com valores elevados resulta em nível moderado de ansiedade
      ctrl.Rule(self.freq_cardiaca['elevada'] | self.preocupacao['alto'] | self.sono['ruim'] | self.tensao['tensa'], self.ansiedade['moderado']),

      # Regra 5: Frequência cardíaca normal, baixo nível de preocupação, sono bom ou regular, tensão muscular relaxada
      # Resulta em baixo nível de ansiedade
      ctrl.Rule(self.freq_cardiaca['normal'] & self.preocupacao['baixo'] & (self.sono['boa'] | self.sono['regular']) & self.tensao['relaxada'], self.ansiedade['baixo']),

      # Regra 6: Frequência cardíaca elevada, baixo nível de preocupação, bom sono, tensão muscular relaxada
      # Resulta em nível moderado de ansiedade
      ctrl.Rule(self.freq_cardiaca['elevada'] & self.preocupacao['baixo'] & self.sono['boa'] & self.tensao['relaxada'], self.ansiedade['moderado']),

      # Regra 7: Frequência cardíaca muito elevada, moderada preocupação, sono ruim, tensão muscular tensa
      # Resulta em alto nível de ansiedade
      ctrl.Rule(self.freq_cardiaca['muito_elevada'] & self.preocupacao['moderado'] & self.sono['ruim'] & self.tensao['tensa'], self.ansiedade['alto']),

      # Regra 8: Frequência cardíaca normal, moderada preocupação, sono ruim, tensão muscular tensa
      # Resulta em nível moderado de ansiedade
      ctrl.Rule(self.freq_cardiaca['normal'] & self.preocupacao['moderado'] & self.sono['ruim'] & self.tensao['tensa'], self.ansiedade['moderado']),

      # Regra 9: Frequência cardíaca elevada, alta preocupação, bom sono, tensão muscular relaxada
      # Resulta em alto nível de ansiedade
      ctrl.Rule(self.freq_cardiaca['elevada'] & self.preocupacao['alto'] & self.sono['boa'] & self.tensao['relaxada'], self.ansiedade['alto']),

      # Regra 10: Frequência cardíaca muito elevada, baixo nível de preocupação, bom sono, tensão muscular moderada
      # Resulta em nível moderado de ansiedade
      ctrl.Rule(self.freq_cardiaca['muito_elevada'] & self.preocupacao['baixo'] & self.sono['boa'] & self.tensao['moderada'], self.ansiedade['moderado']),

      # Regra 11: Frequência cardíaca normal, alta preocupação, sono regular, tensão muscular tensa
      # Resulta em alto nível de ansiedade
      ctrl.Rule(self.freq_cardiaca['normal'] & self.preocupacao['alto'] & self.sono['regular'] & self.tensao['tensa'], self.ansiedade['alto']),

      # Regra 12: Frequência cardíaca elevada, moderada preocupação, sono ruim, tensão muscular relaxada
      # Resulta em alto nível de ansiedade
      ctrl.Rule(self.freq_cardiaca['elevada'] & self.preocupacao['moderado'] & self.sono['ruim'] & self.tensao['relaxada'], self.ansiedade['alto']),

      # Regra 13: Frequência cardíaca normal, moderada preocupação, bom sono, tensão muscular moderada
      # Resulta em nível moderado de ansiedade
      ctrl.Rule(self.freq_cardiaca['normal'] & self.preocupacao['moderado'] & self.sono['boa'] & self.tensao['moderada'], self.ansiedade['moderado']),

      # Regra 14: Frequência cardíaca muito elevada, alta preocupação, sono ruim, tensão muscular relaxada
      # Resulta em alto nível de ansiedade
      ctrl.Rule(self.freq_cardiaca['muito_elevada'] & self.preocupacao['alto'] & self.sono['ruim'] & self.tensao['relaxada'], self.ansiedade['alto'])
    ]

  def diagnostico_ansiedade(self, freq_card, nivel_preoc, qual_sono, tensao_musc, metodo_defuzz='centroid'):
    """
      Realiza o diagnóstico de ansiedade com base nos parâmetros fornecidos.

      Args:
          freq_card (float): Frequência cardíaca.
          nivel_preoc (float): Nível de preocupação.
          qual_sono (float): Qualidade do sono.
          tensao_musc (float): Tensão muscular.
          metodo_defuzz (str): Método de defuzzificação (padrão: 'centroid').

      Returns:
          str: Diagnóstico textual do nível de ansiedade.
    """
    # Atribuição dos valores de entrada ao sistema
    self.simulacao.input['frequencia_cardiaca'] = freq_card
    self.simulacao.input['nivel_preocupacao'] = nivel_preoc
    self.simulacao.input['qualidade_sono'] = qual_sono
    self.simulacao.input['tensao_muscular'] = tensao_musc

    # Definição do método de defuzzificação e computação do resultado
    self.ansiedade.defuzzify_method = metodo_defuzz
    self.simulacao.compute()

    # Obtenção e interpretação do resultado
    nivel_ansiedade = self.simulacao.output['nivel_ansiedade']
    print(f"Nível de Ansiedade ({metodo_defuzz}): {nivel_ansiedade:.2f}")

    # Classificação do nível de ansiedade
    if nivel_ansiedade < 30:
        return "Baixo nível de ansiedade"
    elif 30 <= nivel_ansiedade < 60:
        return "Nível moderado de ansiedade"
    else:
        return "Alto nível de ansiedade"


  def plotar_grafico_individual(self, variavel, titulo, entrada=None):
    """
      Plota o gráfico de uma variável fuzzy individual.

      Args:
          variavel (Antecedent ou Consequent): Variável fuzzy a ser plotada.
          titulo (str): Título do gráfico.
          entrada (float, opcional): Valor de entrada para visualização.
    """
    plt.figure(figsize=(8, 4))
    variavel.view(sim=self.simulacao)
    plt.title(titulo)
    plt.ylabel('Pertinência')
    plt.xlabel(titulo)
    plt.legend()
    plt.tight_layout()
    plt.show()


  def plotar_graficos(self, freq_card, nivel_preoc, qual_sono, tensao_musc):
    """
      Plota os gráficos de todas as variáveis fuzzy do sistema.

      Args:
          freq_card (float): Frequência cardíaca.
          nivel_preoc (float): Nível de preocupação.
          qual_sono (float): Qualidade do sono.
          tensao_musc (float): Tensão muscular.
    """
    # Atualização dos valores de entrada
    self.simulacao.input['frequencia_cardiaca'] = freq_card
    self.simulacao.input['nivel_preocupacao'] = nivel_preoc
    self.simulacao.input['qualidade_sono'] = qual_sono
    self.simulacao.input['tensao_muscular'] = tensao_musc
    self.simulacao.compute()

    # Plotagem dos gráficos individuais
    self.plotar_grafico_individual(self.freq_cardiaca, 'Frequência Cardíaca', freq_card)
    self.plotar_grafico_individual(self.preocupacao, 'Nível de Preocupação', nivel_preoc)
    self.plotar_grafico_individual(self.sono, 'Qualidade do Sono', qual_sono)
    self.plotar_grafico_individual(self.tensao, 'Tensão Muscular', tensao_musc)
    self.plotar_grafico_individual(self.ansiedade, 'Nível de Ansiedade', self.simulacao.output['nivel_ansiedade'])


def entrada_manual(diagnostico_fuzzy, metodo_defuzz='centroid'):
  """
    Permite a entrada manual dos dados do paciente e realiza o diagnóstico.

    Esta função solicita ao usuário que insira os valores para frequência cardíaca,
    nível de preocupação, qualidade do sono e tensão muscular. Em seguida, realiza
    o diagnóstico de ansiedade usando o sistema fuzzy.

    Args:
        diagnostico_fuzzy (DiagnosticoAnsiedadeFuzzy): Instância do sistema de diagnóstico fuzzy.
        metodo_defuzz (str): Método de defuzzificação a ser utilizado (padrão: 'centroid').
  """

  try:
    # Solicitação de entrada dos dados do paciente
    freq_card = float(input("Digite a frequência cardíaca (60-120 bpm): "))
    nivel_preoc = float(input("Digite o nível de preocupação (0-10): "))
    qual_sono = float(input("Digite a qualidade do sono (0-10, onde 10 é ótimo): "))
    tensao_musc = float(input("Digite o nível de tensão muscular (0-10): "))

    # Verificação se os valores estão dentro dos intervalos permitidos
    if not (60 <= freq_card <= 120 and 0 <= nivel_preoc <= 10 and 0 <= qual_sono <= 10 and 0 <= tensao_musc <= 10):
      print("Valores fora dos intervalos permitidos.")
      return

    # Realização do diagnóstico e exibição do resultado
    resultado = diagnostico_fuzzy.diagnostico_ansiedade(freq_card, nivel_preoc, qual_sono, tensao_musc, metodo_defuzz)
    print(f"Resultado: {resultado}")

    # Plotagem dos gráficos para visualização
    diagnostico_fuzzy.plotar_graficos(freq_card, nivel_preoc, qual_sono, tensao_musc)
  except ValueError:
    print("Entrada inválida. Por favor, insira valores numéricos.")


def casos_de_teste(diagnostico_fuzzy):
    """
      Executa casos de teste pré-definidos para o sistema de diagnóstico de ansiedade.

      Esta função roda uma série de casos de teste com diferentes combinações de
      valores de entrada, utilizando vários métodos de defuzzificação.

      Args:
          diagnostico_fuzzy (DiagnosticoAnsiedadeFuzzy): Instância do sistema de diagnóstico fuzzy.
    """

    print("\nExecutando Casos de Teste...")

    # Definição dos casos de teste
    casos = [
        (65, 2, 8, 1),   # Caso 1: Baixo
        (80, 5, 5, 5),   # Caso 2: Moderado
        (110, 9, 2, 9),  # Caso 3: Alto
        (70, 3, 9, 2),   # Caso 4: Baixo
        (90, 6, 4, 6),   # Caso 5: Moderado
        (100, 4, 7, 4),  # Caso 6: Moderado
        (75, 1, 10, 3),  # Caso 7: Baixo
        (95, 7, 3, 7),   # Caso 8: Moderado
        (105, 8, 1, 8),  # Caso 9: Alto
        (85, 5, 6, 5)    # Caso 10: Moderado
    ]

    # Métodos de Deffuzificação a serem testados
    metodos = ['centroid', 'bisector', 'mom', 'som', 'lom']

    # Execução dos casos de teste
    for i, caso in enumerate(casos):
      freq_card, nivel_preoc, qual_sono, tensao_musc = caso
      print(f"\nCaso {i + 1}: FC={freq_card}, Preocupação={nivel_preoc}, Sono={qual_sono}, Tensão={tensao_musc}")

      # Testando cada método de deffuzificação
      for metodo in metodos:
        resultado = diagnostico_fuzzy.diagnostico_ansiedade(freq_card, nivel_preoc, qual_sono, tensao_musc, metodo)
        print(f"  Método {metodo}: {resultado}")

      # Plotagem dos gráficos para o caso atual
      diagnostico_fuzzy.plotar_graficos(freq_card, nivel_preoc, qual_sono, tensao_musc)

      # Controle de fluxo para o usuário (continuar ou sair)
      while True:
        print("\nPressione ENTER para continuar para o próximo caso ou 'q' para sair:")
        resposta = input()

        if resposta.lower() == 'q':
          return
        elif resposta == '':
          break
        else:
          print("Opção inválida. Pressione ENTER para continuar ou 'q' para sair.")

    print("Todos os casos de teste foram executados.")


def submenu(diagnostico_fuzzy):
  """
    Exibe o submenu de métodos de desfuzificação e processa a escolha do usuário.

    Esta função apresenta um submenu com diferentes métodos de defuzzificação
    e chama a função de entrada manual com o método escolhido.

    Args:
        diagnostico_fuzzy (DiagnosticoAnsiedadeFuzzy): Instância do sistema de diagnóstico fuzzy.
  """

  while True:
    print("\n")
    print("#===#==#==#==#==#==#==#==#==#==#==#==#===#")
    print("|   Submenu - Métodos de Desfuzificação  |")
    print("#===#==#==#==#==#==#==#==#==#==#==#==#===#")
    print("|         1. Centroid                    |")
    print("|         2. Bisector                    |")
    print("|         3. MOM (Mean of Maximum)       |")
    print("|         4. SOM (Smallest of Maximum)   |")
    print("|         5. LOM (Largest of Maximum)    |")
    print("|         6. Voltar ao menu principal    |")
    print("#===#==#==#==#==#==#==#==#==#==#==#==#===#")
    opcao = input("\nEscolha uma opção: ")

    if opcao == '1':
        entrada_manual(diagnostico_fuzzy, metodo_defuzz='centroid')
    elif opcao == '2':
        entrada_manual(diagnostico_fuzzy, metodo_defuzz='bisector')
    elif opcao == '3':
        entrada_manual(diagnostico_fuzzy, metodo_defuzz='mom')
    elif opcao == '4':
        entrada_manual(diagnostico_fuzzy, metodo_defuzz='som')
    elif opcao == '5':
        entrada_manual(diagnostico_fuzzy, metodo_defuzz='lom')
    elif opcao == '6':
        break
    else:
        print("Opção inválida. Por favor, escolha uma opção válida.")


def menu_principal():
  """
    Exibe o menu principal e gerencia as opções do usuário.

    Esta função cria uma instância do sistema de diagnóstico fuzzy e
    apresenta um menu com opções para entrada manual, execução de testes
    ou saída do programa.
  """

  diagnostico_fuzzy = DiagnosticoAnsiedadeFuzzy()

  while True:
    # Exibição do menu principal
    print("\n")
    print("#===#==#==#==#==#==#==#==#==#==#==#==#===#")
    print("|  Sistema de Diagnóstico de Ansiedade   |")
    print("#===#==#==#==#==#==#==#==#==#==#==#==#===#")
    print("|          1. Entrada manual             |")
    print("|          2. Executar Testes            |")
    print("|          3. Sair                       |")
    print("#===#==#==#==#==#==#==#==#==#==#==#==#===#")
    opcao = input("\nEscolha uma opção: ")

    if opcao == '1':
        submenu(diagnostico_fuzzy)
    elif opcao == '2':
        casos_de_teste(diagnostico_fuzzy)
    elif opcao == '3':
        print("Saindo do programa.")
        break
    else:
        print("Opção inválida. Por favor, escolha uma opção válida.")


if __name__ == "__main__":
    menu_principal()