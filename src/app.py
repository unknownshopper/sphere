from flask import Flask, render_template, request, send_file
import os
from sphere import create_360_gallery
from datetime import datetime
from PIL import Image  # Add this import

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
STATIC_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')

# Create necessary directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)

def auto_adjust_image(image_path):
    """Auto adjust image to meet requirements"""
    with Image.open(image_path) as img:
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize maintaining aspect ratio
        target_size = (1500, 1500)  # Each quadrant should be 1500x1500 for 6000x3000 final image
        img.thumbnail(target_size, Image.Resampling.LANCZOS)
        
        # Create new image with exact dimensions
        new_img = Image.new('RGB', target_size, (0, 0, 0))
        new_img.paste(img, ((target_size[0] - img.size[0]) // 2,
                           (target_size[1] - img.size[1]) // 2))
        
        # Save adjusted image
        new_img.save(image_path, 'PNG', quality=95)

@app.route('/', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        files = {}
        for position in ['front', 'back', 'left', 'right']:
            file = request.files[position]
            if file:
                filename = f"{position}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
                auto_adjust_image(filepath)  # Auto adjust after saving
                files[position] = filepath
        
        if len(files) == 4:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(STATIC_FOLDER, f"360photo_{timestamp}.jpg")
            
            # Create the 360 image with updated metadata
            create_360_gallery(
                files['front'],
                files['back'],
                files['left'],
                files['right'],
                output_path,
                width=6000,
                height=3000
            )
            
            # Add Facebook-specific metadata using exiftool
            os.system(f'exiftool -XMP-GPano:ProjectionType="equirectangular" '
                     f'-XMP-GPano:UsePanoramaViewer=true '
                     f'-XMP-GPano:FullPanoWidthPixels=6000 '
                     f'-XMP-GPano:FullPanoHeightPixels=3000 '
                     f'-XMP-GPano:CroppedAreaImageWidthPixels=6000 '
                     f'-XMP-GPano:CroppedAreaImageHeightPixels=3000 '
                     f'-XMP-GPano:CroppedAreaLeftPixels=0 '
                     f'-XMP-GPano:CroppedAreaTopPixels=0 '
                     f'-overwrite_original {output_path}')
            
            return send_file(output_path, as_attachment=True)
    
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)