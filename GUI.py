import streamlit as st
from PIL import Image

st.title("Safety Distance between cars using OpenCV & Yolo")

# Upload image
image = Image.open(r'D:\UTEX\HK2 2022-2023\Xử lý ảnh\Anh nhom.png')
st.image(image)

# Button
button1_clicked = st.button("Open input video")
button2_clicked = st.button("Open output video")
if button1_clicked:
    video_file = open(r'D:\UTEX\HK2 2022-2023\Xử lý ảnh\cars 1.mp4', 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)

if button2_clicked:
    video_file = open(r'D:\UTEX\HK2 2022-2023\Xử lý ảnh\Output Video.mp4', 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)

    # input_video = cv2.VideoCapture('cars 1.mp4')
    #
    # width = int(input_video.get(cv2.CAP_PROP_FRAME_WIDTH))
    # height = int(input_video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # fps = input_video.get(cv2.CAP_PROP_FPS)
    #
    # output_filename = 'output_video.mp4'
    # fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Choose the appropriate codec
    # output_video = cv2.VideoWriter(output_filename, fourcc, fps, (width, height))
    # ............code............

    # Write the frame to the output video
    # output_video.write(frame)
# input_video.release()
# output_video.release()
