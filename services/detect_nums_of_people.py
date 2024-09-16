import cv2
import numpy as np
from collections import Counter

def get_face_embedding(img_path, model):
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    faces = model.get(img)
    
    if len(faces) == 0:
        return 
    face_embeddings = []
    for face in faces:
        face_embeddings.append(face.embedding)
    return face_embeddings

def detect_nums_of_people(img_path, model):
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    faces = model.get(img)
    print(f'Có {len(faces)} trong khung hình!')
    return len(faces)

def cosine_similarity(a, b):
    if a is None or b is None: return 0

    if len(a) == 0 or len(b) == 0: return 0

    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)

    if norm_a == 0 or norm_b == 0: return 0

    return np.dot(a, b) / (norm_a * norm_b)


def calc_cosine_similarity(embedding, faces_data):
    res = []
    for _ in faces_data:
        person = []
        for key in _.keys():
            if key == "embedding":
                face_embedding = _["embedding"][0]
                cosine_sim = cosine_similarity(embedding, face_embedding)
                person.append(cosine_sim)
            else:
                person.append(_[key])
        res.append(person)
    res = [ _ for _ in res if _[2] > 0.35]
    return sorted(res, key = lambda x: x[2], reverse = True)

def KNN(embedding, faces_data):
    sorted_distance = calc_cosine_similarity(embedding, faces_data)
    if len(sorted_distance) > 5:
        closest_5_embed = sorted_distance[0:5:1]
    else:
        closest_5_embed = sorted_distance
    names = [item[1] for item in closest_5_embed]
    name_counts = Counter(names)
    try:
        most_name = name_counts.most_common(1)[0][0]
        most_list = [ _ for _ in closest_5_embed if _[1] == most_name]
        most_list.sort(key = lambda x: x[2], reverse = True)
        result = most_list[0]
        result = [{
            "id": result[0],
            "name": result[1],
            "role": result[3],
            "position": result[4],
            "department": result[5]
        }]
        print(f'Tìm thấy: {result}')
        return result
    except:
        return [{
            "name": "Khách",
            "role": "Khách"
        }]

def face_recognition(img_path, model, faces_data):
    face_embeddings = get_face_embedding(img_path, model)
    res = []
    for face_embedding in face_embeddings:
        person = KNN(face_embedding, faces_data)
        res.append(person)
    return res