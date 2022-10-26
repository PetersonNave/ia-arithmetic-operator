'''
# this will train your model and might take a little while
load_or_train = input('Você deseja treinar um novo modelo ou carregar o modelo salvo?(treinar/carregar): ')

if load_or_train.lower() == 'treinar':
    myproject = MLforKidsImageProject(key)
    myproject.train_model()
else:
    myproject = UseSalvedModel()
    myproject.load_model()

from mlforkids import MLforKidsImageProject
'''

import os
from use_salved_model import UseSalvedModel
from segmentacao import executar_segmentacao
import PySimpleGUI as sg

# treat this key like a password and keep it secret!
key = "0b9bc1f0-4446-11ed-9c85-e9175b095422a46f8bf5-ac45-4c45-8d5e-344a7aa7139e"

#Carregando o modelo salvo
myproject = UseSalvedModel()
myproject.load_model()

#FUNÇÃO PARA REALIZAR A SEGMENTAÇÃO E OS CÁLCULOS COM A IA.
def realizar_calculo(caminho_da_imagem):

    executar_segmentacao(caminho_da_imagem)

    # Caminho das imagens segmentadas
    path = os.getcwd()
    caminho = path + r"\tools\.temp_images"

    filelist = [f for f in os.listdir(caminho)]
    
    item_lista = []
    confiancas = []

    for file in filelist:

        imagem = myproject.prediction("./tools/.temp_images/" + file)
            
        label = imagem["class_name"]
        confidence = imagem["confidence"]

        item_lista.append((label,str(int(confidence))+"%"))
        confiancas.append(confidence)

    number_1 = ''
    number_2 = ''
    find_operator = False
    operation = ''
    for m in item_lista:
        if not find_operator:
            if not m[0] in ['soma', 'subtracao','divisao','multiplicacao']:
                number_1 += m[0]
            else: 
                find_operator = True
                operation = m[0]
        else:
            number_2 += m[0]

    try:
        if operation == 'soma':
            result = int(number_1) + int(number_2)
            operation = '+'
        elif operation == 'subtracao':
            result = int(number_1) - int(number_2)
            operation = '-'
        elif operation == 'divisao':
            result = int(number_1) / int(number_2)
            operation = '÷'
        elif operation == 'multiplicacao':
            result = int(number_1) * int(number_2)
            operation = '*'
    
    except:
        return "Erro"

    else:
        soma_confiancas = 0

        for c in confiancas:
            soma_confiancas += c

        confianca_geral = int(soma_confiancas/(len(confiancas)))

        print(item_lista)

        for f in filelist:
            os.remove(os.path.join(caminho , f))
        os.rmdir(caminho)

        try:
            return [number_1,operation,number_2,result,confianca_geral]
        except:
            return "Erro"

#INTERFACE
class Tela:
    def __init__(self) -> None:

        #Tema
        sg.theme('Dark Blue 3')

        self.path = os.getcwd()
        
        #Layout
        layout = [
            [sg.Text('Nome do arquivo')],
            [sg.Input(size = (23,1), key = 'filename'), sg.FileBrowse('Procurar', size = (9,1), key = 'filefound', file_types=(("Imagens", "*.png"),("Imagens", "*.jpg"))), sg.Button('Calcular', size = (9,1), key = "calcular")],
            [sg.Checkbox('Continuar utilizando o mesmo arquivo', size = (30,1), key = 'continuar')],
            [sg.Multiline('Seja bem-vindo ao Operador Aritmético!\n\nDigite o nome do arquivo que está na mesma pasta do executável sem a extensão ou procure o arquivo pelo computador.\n\n+ = Soma\n- = Subtração\n* = Multiplicação\n÷ = Divisão\n\n',size=(47,10), key = 'multiline')]
        ]

        #Janela
        self.janela = sg.Window("Operador Aritmético").layout(layout)

    def iniciar(self):

        self.imagem_na_memoria = ''

        while True: #while para a tela não fechar

            #Extrair dados da janela
            self.events, self.values = self.janela.Read()
            multiline = self.janela['multiline']

            #Fechar aplicação
            if self.events == sg.WIN_CLOSED:
                break

            #Botão calcular ativado
            if self.events == 'calcular':
                filename = self.values['filename']
                filefound = self.values['filefound']
                continuar = self.values['continuar']

                #Caso deseje usar a imagem da memória
                if continuar:
                    if self.imagem_na_memoria == '':
                        multiline.print("Não há imagem na memória.\n")

                    else:
                        retorno = realizar_calculo(self.imagem_na_memoria)
                        if retorno == "Erro":
                            multiline.print("Não foi possível identificar a imagem.\n")
                        else:
                            number_1 = retorno[0]
                            operation = retorno[1]
                            number_2 = retorno[2]
                            resultado = retorno[3]
                            confianca = retorno[4]

                            if resultado % int(resultado) != 0:
                                resultado = round(resultado,2)

                            multiline.print(f'Resultado: {number_1} {operation} {number_2} = {resultado}')
                            multiline.print(f'Confiança: {confianca}%\n')

                #Caso não seja digitado e nem selecionado nada
                elif filefound == '' and filename == '':
                    multiline.print("Nenhum arquivo selecionado.\n")

                #Caso o arquivo buscado for diferente do nome buscado, ele dará prioridade ou digitado
                elif filename != filefound:

                    #Iremos conferir se o arquivo existe em png ou jpg
                    filename_com_extensao = filename + ".png"
                    arquivo = self.path + r"\\" + filename_com_extensao
                    existe = os.path.exists(arquivo)

                    if not existe:
                        filename_com_extensao = filename + ".jpg"
                        arquivo = self.path + r"\\" + filename_com_extensao
                        existe = os.path.exists(arquivo)

                    #Se existir aplicaremos os cálculos
                    if existe:
                        self.imagem_na_memoria = arquivo
                        retorno = realizar_calculo(self.imagem_na_memoria)
                        if retorno == "Erro":
                            multiline.print("Não foi possível identificar a imagem.\n")
                        else:
                            number_1 = retorno[0]
                            operation = retorno[1]
                            number_2 = retorno[2]
                            resultado = retorno[3]
                            confianca = retorno[4]

                            if resultado % int(resultado) != 0:
                                resultado = round(resultado,2)

                            multiline.print(f'Resultado: {number_1} {operation} {number_2} = {resultado}')
                            multiline.print(f'Confiança: {confianca}%\n')

                    else:
                        multiline.print("Arquivo não existente.\n")

                #Usaremos o diretório passado pelo usuário
                else:
                    self.imagem_na_memoria = filefound
                    retorno = realizar_calculo(self.imagem_na_memoria)
                    if retorno == "Erro":
                        multiline.print("Não foi possível identificar a imagem.\n")
                    else:
                        number_1 = retorno[0]
                        operation = retorno[1]
                        number_2 = retorno[2]
                        resultado = retorno[3]
                        confianca = retorno[4]

                        if resultado % int(resultado) != 0:
                            resultado = round(resultado,2)

                        multiline.print(f'Resultado: {number_1} {operation} {number_2} = {resultado}')
                        multiline.print(f'Confiança: {confianca}%\n')

#lIGANDO A INTERFACE
tela = Tela()
tela.iniciar()