# File struture
```bash
├── app                                 # "app" is a Python package
│   ├── __init__.py                     # this file makes "app" a "Python package"
│   ├── main.py                         # "main" module, e.g. import app.main
│   ├── .env                            # environment
│   ├── data                            # data folder for storing data and images
│   │   ├── img                         # images folder for storing images
│   │   │   │   personal data folder    
│   │   │   └── data.json               
│   │   └── lichTuan                    
│   │       └── lichTuan.docx           
│   ├── database                        # makes "routers" a "Python subpackage"
│   │   ├── __init__.py                 
│   │   ├── database.py                
│   │   └── user.db
│   ├── routers                         # makes "routers" a "Python subpackage"
│   │   ├── __init__.py                 # this file makes "routers" a "Python package"
│   │   ├── access_data.py              # submodule for accessing data
│   │   ├── auth.py                     # submodule for authorizing users
│   │   └── face_recognition.py         # submodule for face recognition
│   ├── internal                        # "internal" is a "Python subpackage"
│   │   ├── __init__.py                 
│   │   └── admin.py                    
│   ├── internal                        # makes "internal" a "Python subpackage"
│   │   ├── __init__.py
│   │   ├── base_model.py
│   │   ├── dependencies.py
│   │   └── received_img.png
├── README.md
├── .env
├── API_management.txt                       
└── requirement.txt                           
```