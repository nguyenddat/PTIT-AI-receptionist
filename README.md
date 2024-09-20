# File struture
```bash
├── app                             # "app" is a Python package
│   ├── __init__.py                 # this file makes "app" a "Python package"
│   ├── main.py                     # "main" module, e.g. import app.main
│   ├── data                        # data folder for storing data and images
│   │   ├── img                     # images folder for storing images
│   │   └── data.json               # json file for storing users' data
│   ├── routers                     # makes "routers" a "Python subpackage"
│   │   ├── __init__.py             # this file makes "routers" a "Python package"
│   │   ├── dependencies.py         # "dependencies" module, e.g. import app.dependencies
│   │   ├── base_model.py           # define classes
│   │   ├── access_data.py          # "access_data" submodule, e.g. import app.routers.items
│   │   └── face_recognition.py     # "face_recognition" submodule, e.g. import app.routers.users
│   └── internal                    # "internal" is a "Python subpackage"
│       ├── __init__.py             # makes "internal" a "Python subpackage"
│       └── admin.py                # "admin" submodule, e.g. import app.internal.admin
├── README.md                       
├── requirement.txt                           
```



## Quản lý API/WebSocket

### Access Data API

#### `<GET/ WebSocket> /api/get-identity`
- Nhận thông tin được post từ máy đọc CCCD và đẩy thẳng sang máy khách thông qua WebSocket đã kết nối từ trước đó.
    - *Dữ liệu nhận:*
    ```json
    {
        "Identity Code": "",
        "Name": "",
        "DOB": "",
        "Gender": "",
        "Nationality": "",
        "Ethnic": "",
        "Religion": "",
        "Hometown": "",
        "Permanent Address": "",
        "Identifying Features": "",
        "Card Issuance Date": "",
        "Expiration Date": ""
    }
    ```
    - *Dữ liệu trả về:*
    ```json
    {
        "Identity Code": "",
        "Name": "",
        "DOB": "",
        "Gender": "",
        "Nationality": "",
        "Ethnic": "",
        "Religion": "",
        "Hometown": "",
        "Permanent Address": "",
        "Identifying Features": "",
        "Card Issuance Date": "",
        "Expiration Date": ""
    }
    ```

#### `<POST> /api/post-personal-img`
- Nhận thông tin của khách hàng nhằm đăng ký và lưu dữ liệu khách hàng cho mục đích nhận diện sau đó.
    - *Dữ liệu nhận:*
    ```json
    {
        "b64_img": ["b64", "b64", ....],
        "cccd": {
            "Identity Code": "",
            "Name": "",
            "DOB": "",
            "Gender": "",
            "Nationality": "",
            "Ethnic": "",
            "Religion": "",
            "Hometown": "",
            "Permanent Address": "",
            "Identifying Features": "",
            "Card Issuance Date": "",
            "Expiration Date": ""
        },
        "role": ""
    }
    ```
    - *Dữ liệu trả về:*
    ```json
    {
        "response": "Upload successfully!" hoặc "Thông tin của quý khách đã tồn tại" hoặc "err"
    }
    ```

#### `<GET> /api/get-all-data`
- Trả về toàn bộ thông tin của khách hàng đã lưu.
    - *Dữ liệu trả về:*
    ```json
    [
        {
            "embedding": "đường dẫn đến file txt lưu embedding",
            "Identity Code": "",
            "Name": "",
            "DOB": "",
            "Gender": "",
            "Hometown": "",
            "role": ""
        }
    ]
    ```

### Face Recognition API

#### `<WebSocket> /ws`
- Trả liên tục thông tin của khách hàng xuất hiện trước camera.
    - *Dữ liệu nhận:* `b64`
    - *Dữ liệu trả về:*
        - *Số lượng người:*
        ```json
        {
            "nums_of_people": "nums_of_people"
        }
        ```
        - *Thông tin khách hàng:*
        ```json
        {
            "person_datas": [
                {
                    "name1": "name1",
                    "role1": "role1"
                },
                {
                    "name2": "name2",
                    "role2": "role2"
                }
            ]
        }
        ```