import qrcode
import cv2
import streamlit as st
from io import BytesIO
from PIL import Image
import numpy as np

def generate_qr(text):
    """Generează un cod QR pe baza textului/URL-ului."""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    return img

def decode_qr(image):
    """Decodare QR code dintr-o imagine."""
    detector = cv2.QRCodeDetector()
    value, _, _ = detector.detectAndDecode(image)
    return value

def scan_qr_from_camera():
    """Scanează un cod QR folosind camera web."""
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()

    stop_button = st.button("Stop Camera")

    stframe = st.empty()
    decoded_value = None

    while True:
        ret, frame = cap.read()
        if not ret:
            st.error("Nu se poate accesa camera.")
            break

        value, _, _ = detector.detectAndDecode(frame)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        stframe.image(frame_rgb, channels="RGB", use_container_width=True)

        if value:
            decoded_value = value
            break

        if stop_button:
            break

    cap.release()
    return decoded_value

def main():
    st.title("QR Code Generator & Decoder")

    tabs = st.selectbox("Alege funcționalitatea", ["Generare QR Code", "Decodare QR Code"])

    if tabs == "Generare QR Code":
        st.subheader("Generează Cod QR")
        text = st.text_input("Introduceți textul sau URL-ul pentru QR Code")

        if text:
            img = generate_qr(text)

            buf = BytesIO()
            img.save(buf, format="PNG")
            buf.seek(0)
            st.image(buf, caption="Codul tău QR", use_container_width=True)

            st.download_button(
                label="Descarcă QR Code-ul",
                data=buf,
                file_name="qr_code.png",
                mime="image/png"
            )

    elif tabs == "Decodare QR Code":
        st.subheader("Decodare Cod QR")

        uploaded_file = st.file_uploader("Încarcă o imagine cu QR code", type=["png", "jpg", "jpeg", "gif"])
        if uploaded_file:
            try:
                pil_image = Image.open(uploaded_file)

                if pil_image.mode != "RGB":
                    pil_image = pil_image.convert("RGB")

                image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

                decoded_text = decode_qr(image)

                if decoded_text:
                    st.success(f"Codul QR conține: {decoded_text}")
                else:
                    st.error("Nu s-a putut decoda codul QR.")
            except Exception as e:
                st.error(f"A apărut o eroare la procesarea imaginii: {e}")

        if st.button("Scanează cu Camera"):
            result = scan_qr_from_camera()
            if result:
                st.success(f"Cod QR detectat: {result}")
            else:
                st.error("Nu s-a detectat niciun Cod QR sau camera a fost oprită.")


if __name__ == "__main__":
    main()