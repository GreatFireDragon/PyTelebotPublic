import telebot
from telebot import types
import os
import cv2    #opencv-python
import commands
import numpy as np


API_KEY = '5263831940:AAGxk7T_bP7eQGDmKeH6sopuVCH7dpY_8bo'
bot = telebot.TeleBot(API_KEY)






# Операции над изображениями
# -----------------------------------------------------------------------
def blur(image, matrix):
    pic = cv2.imread(image)        # Читаю исходное изображение
    cv2.imwrite('output_image.jpg', cv2.blur(pic, matrix))

# -----------------------------------------------------------------------
def chb(image):
    pic = cv2.imread(image)        # Читаю исходное изображение
    image_gray = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('output_image.jpg', image_gray)

# -----------------------------------------------------------------------
def canny(image, matrix):
    pic = cv2.imread(image)        # Читаю исходное изображение
    image = cv2.Canny(pic, matrix[0], matrix[1] )
    cv2.imwrite('output_image.jpg', image)
# -----------------------------------------------------------------------
def mirror_y(image):
    pic = cv2.imread(image)
    img_flip = cv2.flip(pic, 1)
    cv2.imwrite('output_image.jpg', img_flip)

def mirror_x(image):
    pic = cv2.imread(image)
    img_flip = cv2.flip(pic, 0)
    cv2.imwrite('output_image.jpg', img_flip)

# -----------------------------------------------------------------------

def cartoon(img, k):
    # https://projectgurukul.org/cartooning-image-opencv-python/
    # Reading image
    img = cv2.imread(img)

    # Defining input data for clustering
    data = np.float32(img).reshape((-1, 3))

    # Defining criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
    # Applying cv2.kmeans function
    _, label, center = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    center = np.uint8(center)

    # Reshape the output data to the size of input image
    result = center[label.flatten()]
    result = result.reshape(img.shape)

    # Convert the input image to gray scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Perform adaptive threshold
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 9, 8)

    # Smooth the result
    blurred = cv2.medianBlur(result, 3)

    # Combine the result and edges to get final cartoon effect
    cartoon = cv2.bitwise_and(blurred, blurred, mask=edges)

    cv2.imwrite('output_image.jpg', cartoon)



# -----------------------------------------------------------------------
# Next Step Handlers для записи матриц ( для обработки изображений)
# -----------------------------------------------------------------------
def blur_matrix_step(message):

    try:
        matrix = abs(int(message.text))
    except Exception:
        bot.send_message(message.chat.id, text="Матрицей должно быть целое число, попробуйте ещё раз.")
        return

    matrix = (matrix, matrix)
    blur("input_image.jpg", matrix)
    all_done_photo(message.chat.id)

# -----------------------------------------------------------------------
def canny_matrix_step(message):
    try:
        matrix = abs(int(message.text))
    except Exception:
        bot.send_message(message.chat.id, text="Матрицей должно быть целое число, попробуйте ещё раз.")
        return

    matrix = (matrix, matrix*2)

    canny("input_image.jpg", matrix)
    all_done_photo(message.chat.id)
# -----------------------------------------------------------------------
def cartoon_matrix_step(message):

    matrix = int(message.text)
    cartoon("input_image.jpg", matrix)
    all_done_photo(message.chat.id)





# Отправляет фото
# -----------------------------------------------------------------------
def all_done_photo(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = types.KeyboardButton(commands.dict["exit"])
    markup.add(back)

    bot.send_photo(chat_id,
                   open("output_image.jpg", "rb"),
                   caption="Фото после обработки", reply_markup=markup)

    os.remove("input_image.jpg")
    os.remove("output_image.jpg")


# -----------------------------------------------------------------------





