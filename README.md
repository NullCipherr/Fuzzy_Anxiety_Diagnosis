# Sistema de Diagnóstico de Ansiedade Fuzzy 🤖💆‍♂️💡

Bem-vindo ao repositório do **Sistema de Diagnóstico de Ansiedade Fuzzy**! Este projeto utiliza a lógica fuzzy para avaliar o nível de ansiedade com base em quatro parâmetros: frequência cardíaca, nível de preocupação, qualidade do sono e tensão muscular. 🌡️🧠💤💪

## Funcionalidades 🚀

- **Diagnóstico de Ansiedade**: Avaliação precisa do nível de ansiedade usando lógica fuzzy.
- **Gráficos Interativos**: Visualização das variáveis fuzzy e dos resultados.
- **Testes Automatizados**: Execução de casos de teste pré-definidos para validação do sistema.
- **Entrada Manual**: Permite ao usuário inserir dados e obter um diagnóstico em tempo real.

## Como Usar 🛠️

1. **Clone o Repositório**:

   ```sh
   git clone https://github.com/NullCipherr/Fuzzy_Anxiety_Diagnosis.git
   cd Fuzzy_Anxiety_Diagnosis

   ```

2. **Instale as Dependências:**:

   ```sh
   pip install -r requirements.txt

   ```

3. **Execute o Programa**:
   ```sh
   python diagnostico_ansiedade.py
   ```

## Estrutura do Projeto 📁

    diagnostico_ansiedade.py: Script principal com a implementação do sistema de diagnóstico.
    README.md: Instruções e informações sobre o projeto.
    requirements.txt: Lista de dependências necessárias.

## Exemplo de Uso 📊

    ```sh
    from diagnostico_ansiedade import DiagnosticoAnsiedadeFuzzy

    diagnostico = DiagnosticoAnsiedadeFuzzy()
    resultado = diagnostico.diagnostico_ansiedade(80, 5, 5, 5)
    print(resultado)
    diagnostico.plotar_graficos(80, 5, 5, 5)
    ```

## Contribuição 🤝

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.
