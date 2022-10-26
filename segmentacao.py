 # Bibliotecas
import cv2
import os
import numpy as np
from imutils import contours
from PIL import Image 


def verificar_pasta(caminho):
    # Verificar se pasta Repositorio existe
    if os.path.isdir(caminho) == False:
        os.mkdir(caminho)

def deletar_arquivos(caminho):
    filelist = [f for f in os.listdir(caminho)]
    for f in filelist:
        os.remove(os.path.join(caminho , f))

def executar_segmentacao(imagem):

    # Caminho
    path = os.getcwd()
    caminho = path + r"\.temp_images"

    verificar_pasta(caminho)
    deletar_arquivos(caminho)

    # Imagem com os dados
    img = cv2.imread(imagem)

    # Pre-Processamento
    # Imagem em tons de cinza
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Filtro de suavizacao
    img_blur = ROI = cv2.medianBlur(gray, 3)

   
    # Detectcao de bordas
    edges = cv2.Canny(img_blur, 50, 255)

    # Morfologia matematica
    kernel = np.ones((9,9), np.uint8)
    img_dilation = (cv2.dilate(edges, kernel, iterations=1))

    #Imagem final
    img_final = img_blur

    # Segementacao
    ret,thresh1 = cv2.threshold(img_final,127,255,cv2.THRESH_BINARY)

    # Localizar contornos
    # cv2.RETR_TREE -> recupera todos os contornos e reconstrói uma hierarquia completa de contornos aninhados.
    # cv2.CHAIN_APPROX_SIMPLE -> Armazena apenas os pontos iniciais e finais dos contornos detectados.
    cnts = cv2.findContours(img_dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    # Ordenacao dos contornos encontrados
    (cnts, _) = contours.sort_contours(cnts, method='left-to-right')

    ROI_number = 0
    for c in cnts:
        # Calcular a area encontrada nos contornos. Se area maior que 1100 provavelmente e um numero
        area = cv2.contourArea(c)
        if area > 1100 :
            x,y,w,h = cv2.boundingRect(c)  # Coordenadas dos contornos             
            #cv2.rectangle(img, (x - 1, y - 1), (x + 1 + w, y + 1 + h), (0, 0, 255), 1) # Selecionar um retangulo
            ROI = thresh1[y-5:y+h+5, x-10:x+w+10]
            ROI = cv2.resize(ROI, (250,250), interpolation = cv2.INTER_AREA) # Salvar a imagem 1000x1000 (Modelo treinado MNIST)
            #cv2.drawContours(img, [c], -1, (0,255,0), -1) # Desenhar o contorno localizado
            #ROI = cv2.bitwise_not(ROI)
            ROI = cv2.copyMakeBorder(ROI, 100, 100, 100, 100, cv2.BORDER_CONSTANT, value=[255, 255, 255])
            cv2.imwrite(path + f'\\.temp_images\\img_{ROI_number}.jpg', ROI)
            ROI_number += 1