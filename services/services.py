import base64
from PIL import Image
import io

from insightface.app import FaceAnalysis
from insightface.data import get_image


def import_model():
    model = FaceAnalysis(name = 'buffalo_l')
    model.prepare(ctx_id = 0, det_size = (640, 640))
    return model

def save_image(image_data, filename = './services/received_image.png'):
    image_data = image_data.split(',')[1]
    image_binary = base64.b64decode(image_data)
    image = Image.open(io.BytesIO(image_binary))
    image.save(filename)