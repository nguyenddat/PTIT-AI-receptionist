import cv2

def dectect_nums_of_people(img_path, model):
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    faces = model.get(img)
    print(len(faces))
    return len(faces)