from mlforkids import MLforKidsImageProject
from use_salved_model import UseSalvedModel
# treat this key like a password and keep it secret!
key = "0b9bc1f0-4446-11ed-9c85-e9175b095422a46f8bf5-ac45-4c45-8d5e-344a7aa7139e"

# this will train your model and might take a little while
load_or_train = input('Você deseja treinar um novo modelo ou carregar o modelo salvo?(treinar/carregar): ')
if load_or_train.lower() == 'treinar':
    myproject = MLforKidsImageProject(key)
    myproject.train_model()
else:
    myproject = UseSalvedModel()
    myproject.load_model()

arquivo = ''
while arquivo != 'sair':

    try:
        #Escolhendo o arquivo para testar
        arquivo = str(input("Digite o nome do arquivo que está dentro da pasta de testes sem a extensão: "))

        # CHANGE THIS to the image file you want to recognize
        imagem = myproject.prediction("./imagens_testes/" + arquivo + ".jpg")

    except FileNotFoundError:
        print("Arquivo não existente.")

    else:
        
        label = imagem["class_name"]
        confidence = imagem["confidence"]

        # CHANGE THIS to do something different with the result
        print ("result: '%s' with %d%% confidence" % (label, confidence))