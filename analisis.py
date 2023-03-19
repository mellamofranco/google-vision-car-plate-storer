"""
@author:Franco Mosquera Bonasorte
"""
import os
import io
import cv2
from google.cloud import vision
from google.cloud.vision_v1.types import Image, Feature, AnnotateImageRequest
#from google.cloud.vision_v1 import types
from google.cloud import vision_v1
from skimage.io import imshow, imsave,imread,imread
from skimage.draw import polygon_perimeter
from skimage.color import hsv2rgb
from csv import writer
import datetime
import matplotlib.pyplot as plt
import pytesseract
import storer

objetosD = []
confianza=0.8
placas = []

def localize_objects(path,confianza):
    client = vision.ImageAnnotatorClient()

    with open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    objects = client.object_localization(
        image=image).localized_object_annotations

    for object_ in objects:
        if object_.name == "Car" or object_.name == "Person" or object_.name == "License plate" and object_.score > confianza:
            objetosD.append(object_)

    print("objetosD : ",objetosD)

def show_results(path): 
    path = path
    # Mostrar recuadros
    image = imread(path)
    plt.imshow(image)
    plt.axis('off')
    for object_ in objetosD:
        vertices = [(v.x * image.shape[1], v.y * image.shape[0]) for v in object_.bounding_poly.normalized_vertices]
        rr, cc = polygon_perimeter([v[1] for v in vertices], [v[0] for v in vertices], shape=image.shape)
        color = (1, 0, 0) # red color
        image[rr, cc] = color
        plt.plot([v[0] for v in vertices] + [vertices[0][0]], [v[1] for v in vertices] + [vertices[0][1]], linewidth=1, color=color)
        plt.text(vertices[0][0], vertices[0][1], object_.name, fontsize=12, color=color)
    plt.show()

#funcion de OCR para placas
def plate_parser(bounding_poly,path):
    path = path
    image = imread(path)

    # obtener medidas de imagen
    height, width, channels = image.shape
    # descomprimir bouding box
    y_min = int(bounding_poly.normalized_vertices[0].y * height)
    y_max = int(bounding_poly.normalized_vertices[2].y * height)
    x_min = int(bounding_poly.normalized_vertices[0].x * width)
    x_max = int(bounding_poly.normalized_vertices[2].x * width)
    
    #crop 
    min_factor = 1.03
    max_factor = 0.96
    crop_img = image[int(y_min*min_factor):int(y_max*max_factor), int(x_min*min_factor):int(x_max-8)]
    #OCR
    text = pytesseract.image_to_string(crop_img)
    
    print("plate: ",text)
    ## COMENTAR PARA EVITAR PANTALLA CON ANALISIS DE PLACA ----------------------------------------------------
    plt.imshow(crop_img)
    plt.show()
    return(text)
    
def organize_data(path):
    path = path
    #iterar objeto de deteccion objetosD y extraer cantidades e info
    personas = 0 
    autos = 0
    placas = 0
    placas_str = [] 
    for object_ in objetosD:
        if object_.name == "Person":
            personas = personas+1
        elif object_.name == "Car":
            autos = autos+1
        elif object_.name == "License plate":
            placas = placas+1
            vertices = object_.bounding_poly
            placas_str.append(plate_parser(vertices,path))
            
    storer.storer(personas,autos,placas," ".join(placas_str))

def main(path):
    
        #reiniciamos variables 
        global objetosD,placas
        objetosD = []
        placas = []
        
        path = path
        #cargar api key
        json_path = r"YOUR_GOOGLE_VISION_APIKEY.json"
        
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = json_path
        localize_objects(path,confianza)
        
        #graficar analisis en imagen
        ## COMENTAR PARA EVITAR PANTALLA CON ANALISIS DE IMAGEN ------------------------------------------
        show_results(path)
                       
        #organizar y guardar datos
        organize_data(path)
                
        
if __name__ == "__main__":
    main("stills/ford.jpg",)