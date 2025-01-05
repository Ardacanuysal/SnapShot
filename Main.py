from flask import Flask, render_template, Response, request, jsonify
import cv2
import numpy as np

app = Flask(__name__)

# Yüz ve göz algılama için CascadeClassifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Efektler için resimler
heart = cv2.imread('heart.png', cv2.IMREAD_UNCHANGED)
glasses = cv2.imread('glasses.png', cv2.IMREAD_UNCHANGED)
emoji = cv2.imread('emoji.png', cv2.IMREAD_UNCHANGED)
dog = cv2.imread('dog.png', cv2.IMREAD_UNCHANGED)
yellow = cv2.imread('yellow.png', cv2.IMREAD_UNCHANGED)

# Varsayılan simge
current_image = None
dog_encoding = False

def load_image(image_name):
    global current_image
    if image_name == 'heart':
        current_image = heart
    elif image_name == 'glasses':
        current_image = glasses
    elif image_name == 'emoji':
        current_image = emoji
    elif image_name == 'yellow':
        current_image = yellow
    elif image_name == 'Puppy':
        current_image = dog
    else:
        current_image = None

# Sıcaklık ve siyah-beyaz efektleri
temperature_level = 50
bw_level = 0
contrast_level = 50

def overlay_image(frame, overlay, x, y, w, h):
    overlay_resized = cv2.resize(overlay, (w, h))
    if overlay_resized.shape[2] == 4:  # RGBA (transparan)
        for c in range(3):
            frame[y:y + overlay_resized.shape[0], x:x + overlay_resized.shape[1], c] = \
                overlay_resized[..., c] * (overlay_resized[..., 3] / 255.0) + \
                frame[y:y + overlay_resized.shape[0], x:x + overlay_resized.shape[1], c] * \
                (1.0 - overlay_resized[..., 3] / 255.0)
    else:
        frame[y:y + overlay_resized.shape[0], x:x + overlay_resized.shape[1]] = overlay_resized

def generate_frames():
    global temperature_level, bw_level, current_image, contrast_level
    cap = cv2.VideoCapture(0)  # Kamerayı açıyoruz
    if not cap.isOpened():
        print("Kamera açılamadı!")
        return

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Kamera görüntüsü alınamadı!")
                break

            frame = cv2.flip(frame, 1)  # Yansıma efekti

            # Kontrast zıtlık efekti
            frame = cv2.convertScaleAbs(frame, alpha=(contrast_level / 50), beta=0)

            # Sıcaklık efekti
            if temperature_level > 50:
                frame = cv2.convertScaleAbs(frame, alpha=(temperature_level / 50), beta=0)
            else:
                frame = cv2.convertScaleAbs(frame, alpha=1, beta=-((50 - temperature_level) * 2))

            # Siyah beyaz efekti
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if bw_level > 0:
                frame = cv2.addWeighted(frame, 1 - bw_level / 100, gray_frame, bw_level / 100, 0)

            # Yüz algılama
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

            for (x, y, w, h) in faces:
                if dog_encoding:
                    cv2.putText(frame, "Dog Encoding Active", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

                if current_image is not None:
                    if current_image is glasses:
                        glasses_width = int(w * 0.75)
                        glasses_height = int(current_image.shape[0] * (glasses_width / current_image.shape[1]))
                        glasses_resized = cv2.resize(current_image, (glasses_width, glasses_height))
                        glasses_x = x + (w - glasses_width) // 2
                        glasses_y = y + h // 4
                        overlay_image(frame, glasses_resized, glasses_x, glasses_y, glasses_width, glasses_height)

                    elif current_image is heart:
                        heart_width = int(w * 0.5)
                        heart_height = int(current_image.shape[0] * (heart_width / current_image.shape[1]))
                        heart_resized = cv2.resize(current_image, (heart_width, heart_height))
                        heart_x = x + (w - heart_width) // 2
                        heart_y = y - heart_height // 2
                        overlay_image(frame, heart_resized, heart_x, heart_y, heart_width, heart_height)

                    elif current_image is emoji:
                        emoji_resized = cv2.resize(current_image, (w, h))
                        overlay_image(frame, emoji_resized, x, y, w, h)

                    elif current_image is dog and dog_encoding:  # Dog görseli aktifse
                        # Yüzün tamamını kaplayacak şekilde dog görselini yeniden boyutlandır
                        dog_resized = cv2.resize(dog, (w, h))  # Yüzün tamamına uyacak şekilde boyutlandır
                        overlay_image(frame, dog_resized, x, y, w, h)  # Yüzün üzerine yerleştir

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    finally:
        cap.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/select_image', methods=['POST'])
def select_image():
    image_name = request.form.get('image', 'emoji')
    load_image(image_name)
    return '', 204

@app.route('/set_contrast', methods=['POST'])
def set_contrast():
    global contrast_level
    data = request.get_json()
    contrast_level = int(data['contrast'])  # Kontrast seviyesini güncelle
    return jsonify(success=True)

@app.route('/start_dog_encoding', methods=['POST'])
def start_dog_encoding():
    global dog_encoding
    dog_encoding = True  # Dog encoding başlatıldı
    return jsonify(success=True)

@app.route('/stop_dog_encoding', methods=['POST'])
def stop_dog_encoding():
    global dog_encoding
    dog_encoding = False  # Dog encoding durduruldu
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True)
