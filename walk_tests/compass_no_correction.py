# -​- encoding: UTF-8 -​-

""" Obtiene datos para incluir en el artículo de Homografía """
from naoqi import ALProxy
import numpy as np

import cv2

NAO_IP = "127.0.0.1"
#NAO_IP = "192.168.2.21"
NAO_PORT = 9559

PI = 3.14159265359

def convert_image(raw_array, height, width):
    """ Convertir imagen naoqi a Mat de OpenCV """
    image_mat = np.zeros((height, width, 3), np.uint8)

    raw_image = raw_array[6]

    values = map(ord, list(raw_image))
    i = 0
    for y in range(0, height):
        for x in range(0, width):
            # itemset is faster than using index,
            # e.g. imageMat[y][x][0] = values[i + 0]
            image_mat.itemset((y, x, 0), values[i + 0])
            image_mat.itemset((y, x, 1), values[i + 1])
            image_mat.itemset((y, x, 2), values[i + 2])
            i += 3

    return image_mat

def display_images(Wz, inliers, referenceImage, currentImage, matchInfo):
    """ Muestra las imágenes en una ventana de OpenCV"""
    """
    # Inicializa los contenedores de imágenes como arreglos de numpy
    imageHeight = 240
    imageWidth = 320
    matchImage = np.zeros((imageHeight*2, imageWidth, 3), np.uint8)

    # Se crea una imagen de correspondencias donde se muestran
    # las imagenes de referencia y la actual.
    for y in range(0, imageHeight):
        for x in range(0, imageWidth):
            matchImage.itemset((x, y), refImage[x][y])
            matchImage.itemset((x, y+240), curImage[x][y])

    for y in range(imageWidth, imageWidth*2):
        for x in range(0, imageWidth):
            matchImage.itemset((x,y), curImage[x][y-240])

    text_buffer = 'Wz: ' + str(Wz)
    # Podría fallar el color del texto
    cv2.putText(curImage, text_buffer, [10, 30],
                cv2.CV_FONT_HERSHEY_PLAIN, 1.0, [255, 255, 255])

    # Averiguar cómo hacer esto en python, no hay CopyTo, específica de C++
    roi = matchImage(cv2.Rect(0,0, 320, 240))
    referenceImage.copyTo(roi)
    roi = matchImage(cv2.Rect(0, 240, 320, 240))
    currentImage.copyTo(roi)

    # Se intenta dibujar las correspondencias
    for i in range(0, inliers):
        # Son variables ALValue
        match = matchInfo[2][matchInfo[3][1][i]]
        refKp = matchInfo[0][match[0]]
        # Es un punto cv2.Point
        ref = cv2.Point(refKp[0][0], refKp[0][1])
        # Es un ALValue
        curKp = matchInfo[1][match[1]]
        # Es un cv2.Point
        cur = cv2.Point(curKp[0][0], curKp[0][1])
        cur.y += 240
        cv2.line(matchImage, cur, ref, [255, 255, 255])
        cv2.circle(matchImage, ref, refKp[1], [255, 255, 255])
        cv2.circle(matchImage, cur, curKp[1], [255, 255, 255])
    """

    cv2.imshow("Reference image", referenceImage)
    cv2.imshow("Current image", currentImage)
    #cv2.imshow("Match", matchImage)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def get_deviation():
    """ Se subscribe a ALVisualCompass para obtener la desviación """
    try:
        memory_proxy = ALProxy("ALMemory", NAO_IP, NAO_PORT)
    except Exception as e:
        print "Error al crear los proxis: "
        print str(e)
        exit(2)

    # Obtenemos los valores de ALMemory
    deviation = memory_proxy.getData("VisualCompass/Deviation")
    match_info = memory_proxy.getData("VisualCompass/Match")

    # Guardamos la desviación con respecto a la rotación sobre el eje Z
    wz_deviation = deviation[0][1]

    # Contamos el número de correspondencias
    matches_size = len(match_info[2])
    inliers_size = len(match_info[3][1])

    # Imprimimos
    print 'wz_deviation en grados = ', wz_deviation * 180.0 / PI
    print 'matches_size = ', matches_size
    print 'inliers_size = ', inliers_size

    # Guardamos los valores en un archivo separado por comas
    file_csv = open('output_no_correction.csv', 'a')
    file_csv.write(str(matches_size) + ',' + str(inliers_size)
                   + ',' + str(wz_deviation) + ',')
    file_csv.close()

    # Regresamos el valor de las desviaciones
    return wz_deviation

def main():
    """Función principal"""
    try:
        # Intenta crear proxis de movimiento
        motion_proxy = ALProxy("ALMotion", NAO_IP, NAO_PORT)
        posture_proxy = ALProxy("ALRobotPosture", NAO_IP, NAO_PORT)
        compass_proxy = ALProxy("ALVisualCompass", NAO_IP, NAO_PORT)
    except Exception as e:
        print "Error al crear los proxis: "
        print str(e)
        exit(2)

    # Se levanta e inicia
    posture_proxy.goToPosture("StandInit", 1.0)

    compass_proxy.enableReferenceRefresh(True)

    # Resolución de la imagen es QVGA (320x240). La hereda de VisualExtractor
    compass_proxy.setResolution(1)

    # Se subcribe al módulo para actualizar los eventos de ALMemory
    compass_proxy.subscribe("VisualCompassTest")

    if NAO_IP != '127.0.0.1':
        # Obtiene las imágenes
        reference_img_array = compass_proxy.getReferenceImage()
        current_img_array = compass_proxy.getCurrentImage()

        reference_img = convert_image(reference_img_array, 240, 320)
        current_img = convert_image(current_img_array, 240, 320)

        # Función para mostrar las imágenes en una ventana de OpenCV
        #display_images(wz_deviation, inliers_size,
        #               reference_img, current_img, match_info)

    # Corregir tres veces
    for i in range(0, 3):
        # Recorrido de 30 cm
        motion_proxy.moveTo(0.3, 0.0, 0.0)
        angle_deviation = (-1) * get_deviation()
        #Rotación sobre el eje Z
        #motion_proxy.moveTo(0.0, 0.0, angle_deviation)


    # Desubscribimos al módulo de ALVisualCompass
    compass_proxy.unsubscribe("VisualCompassTest")
    file_csv = open('output_no_correction.csv', 'a')
    file_csv.write('\n')
    file_csv.close()

    # Termina y se sienta
    posture_proxy.goToPosture("Crouch", 0.4)
    motion_proxy.setStiffnesses("Body", 0.0)

if __name__ == "__main__":
    main()
