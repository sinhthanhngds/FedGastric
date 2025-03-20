import os
import shutil
import math



clinic_path = os.path.expanduser('~/Development/GasHisSDB/160')

# Define source and destination directories
abnormal_source_dir = clinic_path+'/Abnormal'
normal_source_dir = clinic_path+'/Normal'

ab_clinic_dirs = [clinic_path+"/clinic1/abnormal",
               clinic_path+"/clinic2/abnormal",
               clinic_path+"/clinic3/abnormal",
               clinic_path+"/clinic4/abnormal"]

norm_clinic_dirs = [clinic_path+"/clinic1/normal",
                    clinic_path+"/clinic2/normal",
                    clinic_path+"/clinic3/normal",
                    clinic_path+"/clinic4/normal"]

print(ab_clinic_dirs)
print(norm_clinic_dirs)

# Get all files in the source directory
all_normal_files = [f for f in os.listdir(normal_source_dir) if os.path.isfile(os.path.join(normal_source_dir, f))]
all_abnormal_files = [f for f in os.listdir(abnormal_source_dir) if os.path.isfile(os.path.join(abnormal_source_dir, f))]

# Calculate the number of files per clinic
def calc_files_per_clinic(all_files):
    num_files = len(all_files)
    files_per_clinic = math.ceil(num_files / 4)
    print(num_files)
    print(files_per_clinic)
    print(f"There are {num_files} files and {files_per_clinic} files per clinic")
    return files_per_clinic

def copy_file(clinic_dirs, files_per_clinic, source_dir, all_files):
    # Distribute files to each clinic directory ensuring uniqueness
    for i, clinic_dir in enumerate(clinic_dirs):
        # Calculate the range of files for this clinic
        start_index = i * files_per_clinic
        end_index = start_index + files_per_clinic

        # Copy the relevant files to this clinic directory
        for file_name in all_files[start_index:end_index]:
            source_file = os.path.join(source_dir, file_name)
            #print(source_file)
            destination_file = os.path.join(clinic_dir, file_name)
            #print(destination_file)
            shutil.copy(source_file, destination_file)

    print(f"Files have been successfully copied to {', '.join(clinic_dirs)}")

ab_files_per_clinic = calc_files_per_clinic(all_abnormal_files)
norm_files_per_clinic = calc_files_per_clinic(all_normal_files)

copy_file(ab_clinic_dirs, ab_files_per_clinic, abnormal_source_dir, all_abnormal_files)
copy_file(norm_clinic_dirs, norm_files_per_clinic, normal_source_dir, all_normal_files)

