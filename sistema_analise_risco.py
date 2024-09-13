import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Definindo as variáveis fuzzy
historico_credito = ctrl.Antecedent(np.arange(0, 11, 1), 'historico_credito')
renda_mensal = ctrl.Antecedent(np.arange(0, 11, 1), 'renda_mensal')
divida_atual = ctrl.Antecedent(np.arange(0, 11, 1), 'divida_atual')

risco = ctrl.Consequent(np.arange(0, 11, 1), 'risco')
''


#Pertinencia
historico_credito['ruim'] = fuzz.trimf(historico_credito.universe, [0, 0, 3])
historico_credito['regular'] = fuzz.trimf(historico_credito.universe, [2, 5, 7])
historico_credito['bom'] = fuzz.trimf(historico_credito.universe, [6, 8, 10])
historico_credito['excelente'] = fuzz.trimf(historico_credito.universe, [8, 10, 10])

renda_mensal['baixa'] = fuzz.trimf(renda_mensal.universe, [0, 0, 4])
renda_mensal['media'] = fuzz.trimf(renda_mensal.universe, [3, 5, 7])
renda_mensal['alta'] = fuzz.trimf(renda_mensal.universe, [6, 10, 10])

divida_atual['baixa'] = fuzz.trimf(divida_atual.universe, [0, 0, 4])
divida_atual['moderada'] = fuzz.trimf(divida_atual.universe, [3, 5, 7])
divida_atual['alta'] = fuzz.trimf(divida_atual.universe, [6, 10, 10])

risco['baixo'] = fuzz.trimf(risco.universe, [0, 0, 4])
risco['moderado'] = fuzz.trimf(risco.universe, [3, 5, 7])
risco['alto'] = fuzz.trimf(risco.universe, [6, 10, 10])

# Regras fuzzy
rule1 = ctrl.Rule(historico_credito['excelente'] & divida_atual['baixa'], risco['baixo'])

rule2 = ctrl.Rule(historico_credito['ruim'] & divida_atual['alta'], risco['alto'])
rule3 = ctrl.Rule(historico_credito['bom'] & renda_mensal['media'] & divida_atual['moderada'], risco['moderado'])
rule4 = ctrl.Rule(historico_credito['regular'] & divida_atual['moderada'], risco['moderado'])
rule5 = ctrl.Rule(historico_credito['regular'] & divida_atual['alta'], risco['alto'])


risco_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
avaliacao_risco = ctrl.ControlSystemSimulation(risco_ctrl)


# Exemplo de avaliação de cliente
avaliacao_risco.input['historico_credito'] = 7  # "Bom"
avaliacao_risco.input['renda_mensal'] = 5  # "Média"
avaliacao_risco.input['divida_atual'] = 5  # "Moderada"


#Analise do risco
avaliacao_risco.compute()

risco_calculado = round(avaliacao_risco.output['risco'],2)

def interpretar_risco(risco):
    if risco < 3:
        return f"Risco calculado: {risco:.2f}. O risco é BAIXO. O cliente possui um perfil financeiro confiável."
    elif 3 <= risco < 6:
        return f"Risco calculado: {risco:.2f}. O risco é MODERADO. O cliente possui um perfil com algum risco, mas ainda aceitável."
    elif 6 <= risco < 8:
        return f"Risco calculado: {risco:.2f}. O risco é MEDIANO. O cliente apresenta riscos mais elevados, exigindo análise adicional."
    else:
        return f"Risco calculado: {risco:.2f}. O risco é ALTO. O cliente tem um perfil financeiro com elevado risco de inadimplência."


print(interpretar_risco(risco_calculado))