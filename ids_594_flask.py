# -*- coding: utf-8 -*-
"""IDS 594 Flask.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kKZ3s-b72JctWHewifChNgk_gC_QoFb1
"""

# import os
import warnings
warnings.filterwarnings('ignore')

import numpy as np
from PIL import Image, ImageOps
import io

from flask import Flask, request, render_template, flash, redirect, jsonify
import torch
import torchvision.transforms as transforms

global graph

# graph = tf.compat.v1.get_default_graph()

model = torch.load('fer2013_resnet18_model.pkl', map_location=torch.device('cpu'))
model.eval()
app = Flask(__name__)
app.secret_key = 'some secret key'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neural']


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def transform_image(image_bytes):
    my_transforms = transforms.ToTensor()
    image = Image.open(io.BytesIO(image_bytes))
    image = ImageOps.grayscale(image)
    return my_transforms(image).unsqueeze(0)


def get_prediction(image_bytes):
    tensor = transform_image(image_bytes=image_bytes)
    outputs = model.forward(tensor)
    pred = labels[np.argmax(outputs.data.numpy())]
    return pred


@app.route("/", methods=["GET","POST"])
def predict():
  if request.method == 'GET':
      return render_template('index.html')

  if request.method == 'POST':
      if 'file' not in request.files:
          flash('No file')
          return redirect(request.url)

      file = request.files['file']
      if file.filename == '':
          flash('No file')
          return redirect(request.url)

      if file and allowed_file(file.filename):
          image = file.read()

          class_name = get_prediction(image)
          return jsonify({'class_name': class_name})


if __name__ == '__main__':
  app.run()
