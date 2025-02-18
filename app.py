import cv2
import os
import pickle
import numpy as np
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from enhance import image_enhance
from skimage.morphology import skeletonize

# Função para remover pontos indesejados
def removedot(invertThin):
    temp0 = np.array(invertThin[:])
    temp1 = temp0 / 255
    temp2 = np.array(temp1)

    enhanced_img = np.array(temp0)
    filter0 = np.zeros((10, 10))
    W, H = temp0.shape[:2]
    filtersize = 6

    for i in range(W - filtersize):
        for j in range(H - filtersize):
            filter0 = temp1[i:i + filtersize, j:j + filtersize]

            flag = 0
            if sum(filter0[:, 0]) == 0:
                flag += 1
            if sum(filter0[:, filtersize - 1]) == 0:
                flag += 1
            if sum(filter0[0, :]) == 0:
                flag += 1
            if sum(filter0[filtersize - 1, :]) == 0:
                flag += 1
            if flag > 3:
                temp2[i:i + filtersize, j:j + filtersize] = np.zeros((filtersize, filtersize))

    return temp2


# Função para obter os descritores da imagem
def get_descriptors(img):
    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    img = clahe.apply(img)

    # Segmentação da imagem
    img = image_enhance.image_enhance(img)

    # Convertendo a imagem para uint8
    img = np.array(img, dtype=np.uint8)

    # Threshold da imagem
    ret, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    img[img == 255] = 1

    # Thinning (afinamento)
    skeleton = skeletonize(img)
    skeleton = np.array(skeleton, dtype=np.uint8)
    skeleton = removedot(skeleton)

    # Detecção de cantos Harris
    harris_corners = cv2.cornerHarris(img, 3, 3, 0.04)
    harris_normalized = cv2.normalize(harris_corners, 0, 255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32FC1)

    # Extração de keypoints usando os cantos Harris
    threshold_harris = 125
    keypoints = []
    for x in range(0, harris_normalized.shape[0]):
        for y in range(0, harris_normalized.shape[1]):
            if harris_normalized[x][y] > threshold_harris:
                keypoints.append(cv2.KeyPoint(y, x, 1))

    # Criação do descritor ORB
    orb = cv2.ORB_create()

    # Cálculo dos descritores
    _, des = orb.compute(img, keypoints)

    return keypoints, des


# Função principal para obter os descritores a partir de um caminho de imagem
def get_des_input(image_path):
    print(f"Lendo imagem de: {image_path}")
    return get_des(image_path)


# Função para carregar ou gerar descritores para uma imagem
def get_des(image_path):
    if os.path.exists(image_path):
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Lê a imagem em escala de cinza
        kp, des = get_descriptors(img)
        return des
    else:
        raise FileNotFoundError(f"O arquivo {image_path} não existe.")


# Função de comparação com imagens permitidas
def comparisons_with_permitted_images(sample_fingerprint, bf):
    score_threshold = 33

    # Loop pelos usuários cadastrados
    for user in users_authorization_and_authentication():
        permitted_fingerprint = get_des_permitted(user["fingerprint"])
        matches = sorted(bf.match(sample_fingerprint, permitted_fingerprint), key=lambda match: match.distance)

        print(f"Fingerprint do usuário {user['name']} - {user['fingerprint']}")

        score = 0
        for match in matches:
            score += match.distance

        actual_score = score / len(matches)
        print(f"Pontuação real: {actual_score}")

        # Se a pontuação for abaixo do limiar, retorne o usuário
        if actual_score < score_threshold:
            return user
    return None


# Função para carregar ou gerar descritores permitidos
def get_des_permitted(image_name):
    image_pickle = "database/pickles/" + image_name

    # Verifica se o descritor já foi gerado e armazenado
    if os.path.exists(image_pickle):
        print("Carregando descritor a partir do pickle.")
        with open(image_pickle, 'rb') as pickle_file:
            image_desc = pickle.load(pickle_file)
    else:
        print("Gerando novo descritor e armazenando no pickle.")
        image_path = "database/permitted/" + image_name
        image_desc = get_des(image_path)
        with open(image_pickle, 'wb') as pickle_file:
            pickle.dump(image_desc, pickle_file)

    return image_desc


# Função para obter a entrada de imagem e gerar descritores
def users_authorization_and_authentication():
    database = [
        {"name": "101", "fingerprint": "101_1.tif", "level": 1},
        {"name": "102", "fingerprint": "102_1.tif", "level": 1},
        {"name": "103", "fingerprint": "103_1.tif", "level": 1},
        {"name": "104", "fingerprint": "104_1.tif", "level": 1},
        {"name": "105", "fingerprint": "105_1.tif", "level": 2},
        {"name": "106", "fingerprint": "106_1.tif", "level": 2},
        {"name": "107", "fingerprint": "107_1.tif", "level": 2},
        {"name": "108", "fingerprint": "108_1.tif", "level": 3}
    ]
    return database


# Função principal
def main(image_path):
    des = get_des_input(image_path)  # Obtém os descritores da imagem fornecida

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    user = comparisons_with_permitted_images(des, bf)

    if user:
        return user
    else:
        return False


# Função para usar o tkinter e selecionar uma imagem
if __name__ == "__main__":
    Tk().withdraw()  # Não mostra a janela principal do tkinter
    image_path = askopenfilename(title="Escolha uma imagem", filetypes=[("Arquivos de Imagem", "*.jpg;*.jpeg;*.png;*.bmp;*.tif;")])

    if image_path:
        user = main(image_path)
        if user:
            print(f"Usuário encontrado: {user['name']}, Nível: {user['level']}")
        else:
            print("Nenhum usuário correspondente encontrado.")
    else:
        print("Nenhuma imagem foi selecionada.")
