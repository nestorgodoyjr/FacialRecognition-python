# FacialRecognition-python
Install venv
    python3 -m venv venv

Run venv:
    source venv/bin/activate    
Install Required Libraries

    pip install opencv-python
    pip install numpy
    pip install face_recognition
    pip install git+https://github.com/ageitgey/face_recognition_models

        note if you cant install required libraries use pip install <library> --break-system-packages
             if problem installing face_recognition try this pip list | grep setuptools


The face_recognition library also requires dlib, which may need system-specific dependencies. Install dlib using:

    Ubuntu/Debian:
    sudo apt-get install -y cmake g++ make
    pip install dlib

Run:
    python main.py
    or
    python3 main.py