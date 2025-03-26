import cv2
import numpy as np
from PIL import Image

def create_360_gallery(front_image, back_image, left_image, right_image, output_path, width=6000, height=3000):
    # Create a blank canvas with Facebook-compatible dimensions
    canvas = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Calculate dimensions for each image
    img_width = width // 4
    img_height = height // 2
    
    
    # Load and resize all images using PIL instead of cv2
    images = {
        'front': np.array(Image.open(front_image)),
        'back': np.array(Image.open(back_image)),
        'left': np.array(Image.open(left_image)),
        'right': np.array(Image.open(right_image))
    }
    
    # Convert from RGB to BGR for OpenCV processing
    for key in images:
        images[key] = cv2.cvtColor(images[key], cv2.COLOR_RGB2BGR)
    
    # Check if all images were loaded
    for img_name, img in images.items():
        if img is None:
            raise ValueError(f"Could not load image: {img_name}")
    
    # Resize images
    for key in images:
        images[key] = cv2.resize(images[key], (img_width, img_height))
    
    # Place images in the equirectangular format
    # Front (center)
    canvas[height//4:3*height//4, width//4:2*width//4] = images['front']
    # Back (far right and far left - will connect in 360°)
    canvas[height//4:3*height//4, :width//4] = images['back']
    canvas[height//4:3*height//4, 3*width//4:] = images['back']
    # Left
    canvas[height//4:3*height//4, 2*width//4:3*width//4] = images['left']
    # Right
    canvas[height//4:3*height//4, 3*width//4:4*width//4] = images['right']
    
    # Smooth transitions between images
    kernel_size = 31
    canvas = cv2.GaussianBlur(canvas, (kernel_size, kernel_size), 0)
    
    # Save the result with Facebook-specific 360 metadata
    result = Image.fromarray(cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB))
    
    # Create Facebook-specific 360 metadata
    xmp_metadata = '''<x:xmpmeta xmlns:x="adobe:ns:meta/" xmptk="Adobe XMP Core 5.1.0">
        <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
            <rdf:Description rdf:about="" xmlns:GPano="http://ns.google.com/photos/1.0/panorama/">
                <GPano:ProjectionType>equirectangular</GPano:ProjectionType>
                <GPano:FullPanoWidthPixels>6000</GPano:FullPanoWidthPixels>
                <GPano:FullPanoHeightPixels>3000</GPano:FullPanoHeightPixels>
                <GPano:CroppedAreaImageWidthPixels>6000</GPano:CroppedAreaImageWidthPixels>
                <GPano:CroppedAreaImageHeightPixels>3000</GPano:CroppedAreaImageHeightPixels>
                <GPano:CroppedAreaLeftPixels>0</GPano:CroppedAreaLeftPixels>
                <GPano:CroppedAreaTopPixels>0</GPano:CroppedAreaTopPixels>
            </rdf:Description>
        </rdf:RDF>
    </x:xmpmeta>'''

    # Save with XMP metadata
    with open(output_path, 'wb') as f:
        result.save(f, 'JPEG', quality=95)
        f.write(b'\x00')
        f.write(xmp_metadata.encode('utf-8'))

if __name__ == "__main__":
    from datetime import datetime
    
    # Generate unique filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_image = f"galeria_360_{timestamp}.jpg"
    
    # Image paths in the img folder
    front_image = "img/frente.png"
    back_image = "img/atras.png"
    left_image = "img/izq.png"
    right_image = "img/der.png"
    
    create_360_gallery(
        front_image, 
        back_image, 
        left_image, 
        right_image, 
        output_image,
        width=6000,    # Facebook recommended width
        height=3000    # Facebook recommended height
    )