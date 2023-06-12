import cv2
from ultralytics import YOLO
from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

# Initialize YOLO model
model = YOLO('yolov8n.pt')

# Class names for object detection
classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"
              ]


def get_distance(label, height_in_image):
    # Define dimensions for calculating distances
    dimensions = {
        "person": {"real_height": 1.7, "real_distance": 2, "height_per_pixels": 512, "color": (255, 0, 0)},
        "car": {"real_height": 1.4, "real_distance": 2, "height_per_pixels": 336, "color": (0, 255, 127)},
        "bicycle": {"real_height": 0.9, "real_distance": 2, "height_per_pixels": 1, "color": (216, 191, 216)},
        "motorbike": {"real_height": 1.1, "real_distance": 2, "height_per_pixels": 400, "color": (0, 191, 255)},
        "truck": {"real_height": 2.3, "real_distance": 2, "height_per_pixels": 500, "color": (255, 0, 0)},
        "bus": {"real_height": 2.5, "real_distance": 2, "height_per_pixels": 505, "color": (255, 0, 0)}
    }

    # Get the dimensions for the given label
    dimension = dimensions.get(label)

    if dimension:
        real_height = dimension["real_height"]
        real_distance = dimension["real_distance"]
        height_per_pixels = dimension["height_per_pixels"]
        color = dimension["color"]

        # Calculate focal length
        focal_length = float(height_per_pixels * real_distance) / float(real_height)

        # Calculate real distance of the object
        distance = float(focal_length * real_height) / float(height_in_image)

        return distance, color

    return None, None


def check_distance(distance, label):
    if distance < 2:
        return 1
    elif 2 < distance < 5:
        return 2


def load_file():
    if file == "":
        showinfo("Error", "Please select a file")
        return False

    cap = cv2.VideoCapture(file)
    color_green = (0, 255, 127)
    color_red = (0, 0, 255)
    color_yellow = (0, 255, 255)

    while True:
        success, img = cap.read()
        results = model(img, stream=True)

        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                w, h = x2 - x1, y2 - y1
                label = classNames[int(box.cls[0])]

                distance, color = get_distance(label, h)

                if label in ("car", "truck", "person", "bycycle", "motorbike", "bus"):
                    if check_distance(distance, label) == 1:
                        color = color_red
                        cv2.rectangle(img, (0, 0), (1280, 720), color_red, 50)
                    elif check_distance(distance, label) == 2:
                        color = color_yellow

                cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
                text = label + " " + str(round(distance, 2)) + "(m)"
                (w, h), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
                cv2.rectangle(img, (x1, y1 - h - 10), (x1 + w + 30, y1), color, -1)
                cv2.putText(img, text=text, org=(x1, y1), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=0.7,
                            color=(255, 255, 255))

        cv2.imshow('Video Player', img)

        if cv2.waitKey(1) == 13:
            break

    cv2.destroyAllWindows()
    cap.release()


# GUI
def select_frame(name):
    frame_1.place_forget()
    frame_2.place_forget()

    if name == "page1":
        frame_1.place(x=0, y=0, width=1280, height=720)
    elif name == "page2":
        frame_2.place(x=0, y=0, width=1280, height=720)


def select_frame_1():
    select_frame("page1")


def select_frame_2():
    select_frame("page2")


def open_file():
    global file
    filetypes = (
        ('mp4 files', '*.mp4'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    showinfo(
        title='Selected File',
        message=filename
    )
    file = filename


def exit_file():
    pass


def help_information():
    showinfo(
        title='Help Information',
        message='''
        Following below steps: 

        1. Open and select an mp4 file.
        2. Load the file to display.
        3. Press the Enter button to exit the video player.
        4. Use the Exit option in the File menu to exit the GUI.
        '''
    )


def about_information():
    showinfo(
        title='About Information',
        message='''
        This is a project that detects objects and maintains a safe distance between them on the road.

        Authors:
        1. Le Van Manh Quynh 
        2. Ho Quang Huy
        3. Nguyen Huu Duy Tai
        '''
    )


if __name__ == "__main__":
    file = ""
    root = Tk()
    root.title("Video")
    root.geometry("1280x720")

    # First page
    frame_1 = Frame(master=root)
    frame_1.place(x=0, y=0, width=1280, height=720)

    img_logo_ute = ImageTk.PhotoImage(Image.open("Anh nhom.png"))
    label_logo_ute = Label(master=frame_1, image=img_logo_ute)
    label_logo_ute.place(x=0, y=0)

    button = Button(master=frame_1, width=7, height=2, text="Next", command=select_frame_2)
    button.place(x=1200, y=650)

    # Main page
    menu_bar = Menu(master=root)

    file_menu = Menu(master=root, tearoff=0)
    file_menu.add_command(label="Open File", command=open_file)
    file_menu.add_command(label="Load File", command=load_file)
    file_menu.add_command(label="Exit File", command=exit_file)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.destroy)

    menu_bar.add_cascade(label="File", menu=file_menu)

    help_menu = Menu(menu_bar, tearoff=0)
    help_menu.add_command(label="Help Information", command=help_information)
    help_menu.add_command(label="About...", command=about_information)

    menu_bar.add_cascade(label="Help", menu=help_menu)

    root.config(menu=menu_bar)

    frame_2 = Frame(master=root)
    label_vid = Label(master=frame_2)
    label_vid.place(x=0, y=0, width=1280, height=720)

    root.mainloop()
