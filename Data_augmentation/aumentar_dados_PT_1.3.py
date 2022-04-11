from os import chdir,listdir, system, getcwd, path
from cv2 import imread, imshow, imwrite, getRotationMatrix2D, warpAffine, add
import numpy as np

#Com 2 imagens é possível gerar 22 novas imagens
'''Para a rotação o interessante é que imagem tenha um formato e dimensão
Quadrada para não perde proporção'''
 
#Funcão Salvar imagens ('Local', 'image.png')
def salvar (nome,imgRotation):
    imwrite(nome,imgRotation)

#Angulo para girar imagem
angulo = [90,180]

#path local 'Windows'
get_root = getcwd()
#Normaliza path local para unix path 
Norm_root = get_root.replace("\\","/")


#Local das imagens para rotacionar
Input = Norm_root +'/Input'

#local para salvar as imagens
Output = Norm_root+ '/Output'

       

#nome para concatenar junto ao nome da imagem de input
Nomesave=['/90','/180','/Q','/Q90','/Q180']
TestNoise = ['/NN','/N90','/N180','/NQ','/NQ90','/NQ180']

#É importante manter a quantidade de valores no vetor Nomesave equivalente operations1, e o TestNoise a operations2
#_______________________________________________________________

#funcao da biblioteca .os para leitura de dados em diretorio
directory = listdir(Input)
#o chdir altera o diretório de trabalho atual para o caminho dado Input
chdir(Input)

for image in directory:
        #carrega as imagem em Input       
        img = imread(image)
        
        altura, largura = img.shape[:2]
        ponto = (largura / 2, altura / 2) #ponto no centro da figura

        #angulo para rotação    
        Girar90 = getRotationMatrix2D(ponto, angulo[0], 1)
        Girar180 = getRotationMatrix2D(ponto, angulo[1], 1)
        
        #imagem rotacionada   
        rotacao90 = warpAffine(img, Girar90, (largura, altura))
        rotacao180 = warpAffine(img, Girar180, (largura, altura))
        #----------------------------------------------------------
        #quantificar imagem
        r =64
        img_quant = np.uint8(img/r)*r
        img_quant90 = np.uint8(rotacao90/r)*r
        img_quant180 = np.uint8(rotacao180/r)*r

        
        #----------------------------------------------------------
        gauss = np.random.normal(0,1,img.size)
        gauss = gauss.reshape(img.shape[0],img.shape[1],img.shape[2]).astype('uint8')
        
        #Imagem com ruido
        Noiseimg = add(img,gauss)
        Noiseimg90 = add(rotacao90,gauss)
        Noiseimg180 = add(rotacao180,gauss)
        NoiseimgQ = add(img_quant,gauss)
        NoiseimgQ90 = add(img_quant90,gauss)
        NoiseimgQ180 = add(img_quant180,gauss)
        
        operations1 = [(rotacao90),(rotacao180),(img_quant),(img_quant90),(img_quant180)]
        operations2 = [(Noiseimg),(Noiseimg90),(Noiseimg180),(NoiseimgQ),(NoiseimgQ90),(NoiseimgQ180)]

        #ir para a pasta Output      
        #system('cd'+get_root)
        
        #salvas as operacoes 1 
        for Nomeimg in Nomesave:
            for i in range(len(Nomeimg)):
                salvar(Output+Nomeimg+image,operations1[i])

        #ir para a pasta Output      
        #system('cd'+get_root)
        
        #salvas as operacoes 1
        for Nomeimg in TestNoise:
            for i in range(len(TestNoise)):
                salvar(Output+Nomeimg+image,operations2[i])

        #voltar para pasta Input
                
print('Operação completa!!')
print('Verifica pasta Output')
      


