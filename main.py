from flask import Flask, render_template, request, send_file
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import GappedSquareModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.form['data']
    color_option = request.form.get('color_option', 'red_black')  # Default color option
    filename = 'qr_code.png'

    # Generate QR code with a stylish look
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Choose the color gradient based on user selection
    if color_option == 'green_gradient':
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=GappedSquareModuleDrawer(),
            color_mask=RadialGradiantColorMask(
                center_color=(0, 255, 0),  # Green center
                edge_color=(0, 100, 0)  # Dark green edges
            )
        )
    elif color_option == 'blue_gradient':
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=GappedSquareModuleDrawer(),
            color_mask=RadialGradiantColorMask(
                center_color=(0, 0, 255),  # Blue center
                edge_color=(0, 0, 100)  # Dark blue edges
            )
        )
    elif color_option == 'golden_gradient':  # New golden gradient
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=GappedSquareModuleDrawer(),
            color_mask=RadialGradiantColorMask(
                center_color = (204, 153, 0), # Golden center
                edge_color=(139, 69, 19)  # Dark brown edges (chocolate or dark brown)
            )
        )
    else:  # Default red-black gradient
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=GappedSquareModuleDrawer(),
            color_mask=RadialGradiantColorMask(
                center_color=(255, 0, 0),  # Red center
                edge_color=(0, 0, 0)  # Black edges
            )
        )

    img.save(filename)
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
