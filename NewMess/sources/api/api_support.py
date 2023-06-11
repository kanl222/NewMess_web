import io
import base64
from PIL import Image
from flask import request, jsonify, Blueprint

blueprint = Blueprint(
    'api_support',
    __name__,
    template_folder='templates'
)


@blueprint.route('/resize_image', methods=['POST'])
def resize_image():
    if 'image_base64' not in request.form:
        return jsonify({'error': 'No image uploaded'}), 400

    image_base64 = request.form['image_base64']
    image_bytes = base64.b64decode(image_base64)

    encoded_image_base64 = base64.b64encode(process_image(image_bytes)).decode('utf-8')
    response = {
        'data': encoded_image_base64,
        'metadata': {
            'original_filename': None,
            'resized_width': 48,
            'resized_height': 48
        }
    }
    return jsonify(response), 200


def process_image(image_bytes):
    with Image.open(io.BytesIO(image_bytes)) as img:
        img_resized = img.resize((48, 48))
        img_byte_arr = io.BytesIO()
        img_resized.save(img_byte_arr, format='PNG')
        return img_byte_arr.getvalue()
