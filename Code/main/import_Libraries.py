import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os
from skimage.io import imread, imshow
from skimage.transform import resize
from tqdm import tqdm
import random
import tensorflow as tf
import cv2 #<- for interfacing camera and simulating functions
from IPython.display import display, clear_output
import json

import os
from config.definitions import ROOT_DIR
from grayscaleconversionlatest import BinarizeImage