import pydicom
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import os

patient_directory = "/3Dircadb1/3Dircadb1.1/PATIENT_DICOM"
label_directory = "/3Dircadb1/3Dircadb1.1/LABELLED_DICOM"
mask_directory = "/3Dircadb1/3Dircadb1.1/MASKS_DICOM"

patients = []

def add_patient(patient_id, folder_name, folder_path):
    patient = {
        "id": patient_id,
        "folder": folder_name,
        "path" : folder_path
    }
    patients.append(patient)

def find_patients_in_directory(base_directory):
    for folder_name in os.listdir(base_directory):
        folder_path = os.path.join(base_directory, folder_name)
        if os.path.isdir(folder_path) and folder_name.startswith("3Dircadb1."):
            patient_id = int(folder_name.split('3Dircadb1.')[1])
            add_patient(patient_id,folder_name,folder_path)

    patients.sort(key=lambda x:x['id'])

base_directory = "/home/khanh/khanh/IMAGE_PROCESSING/3Dircadb1"
find_patients_in_directory(base_directory)

check = patients[0]
print(check)

""" print("Patient List:")
for patient in patients:
    print(f"Index: {patient['id']}, Folder: {patient['folder']}") """

masks = []
def add_mask_for_patient(patient_id, folder_name):
    mask = {
        "id" : patient_id,
        "label" : folder_name
    }
    masks.append(mask)

def masks_of_patient(patient_id):
    patient_dir = patients[patient_id-1]['path']
    patient_dir += "/MASKS_DICOM"
    for folder_name in os.listdir(patient_dir):
        folder_path = os.path.join(patient_dir,folder_name)
        if os.path.isdir(folder_path):
            add_mask_for_patient(patient_id,folder_name)

    masks.sort(key=lambda x:x['label'])
    return patient_dir

patient_mask_directory = masks_of_patient(1)
print(patient_mask_directory)

def get_label(label):
    label_direct = ""
    for mask in masks:
        if mask['label'] == label:
            label_direct = patient_mask_directory + "/" + str(label)
    return label_direct

label_direct = get_label("bone")
print(label_direct)

""" for mask in masks:
    print(f"Patient ID: {mask['id']}, Label: {mask['label']}") """
    