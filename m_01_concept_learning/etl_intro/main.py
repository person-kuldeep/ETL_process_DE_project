# Contain extact, transform, loading, logging functions.

#required imports
import glob
import pandas as pd
from datetime import datetime
import xml.etree.ElementTree as ET

# Constant variables
log_file = "log_file.txt" 
target_file = "transformed_data.csv" 

#Execution function
def main():
    
    # Log the initialization of the ETL process 
    log_progress("ETL Job Started") 
    
    # Log the beginning of the Extraction process 
    log_progress("Extract phase Started") 
    extracted_data = extract() 
    
    # Log the completion of the Extraction process 
    log_progress("Extract phase Ended") 
    
    # Log the beginning of the Transformation process 
    log_progress("Transform phase Started") 
    transformed_data = transform(extracted_data) 
    print("Transformed Data") 
    print(transformed_data) 
    
    # Log the completion of the Transformation process 
    log_progress("Transform phase Ended") 
    
    # Log the beginning of the Loading process 
    log_progress("Load phase Started") 
    load_data(target_file,transformed_data) 
    
    # Log the completion of the Loading process 
    log_progress("Load phase Ended") 
    
    # Log the completion of the ETL process 
    log_progress("ETL Job Ended") 

#Extract function
def extract_from_csv(file_to_process):
    dataframe =  pd.read_csv(file_to_process)
    return dataframe

def extract_from_json(file_to_process):
    dataframe = pd.read_json(file_to_process, lines=True)
    return dataframe

def extract_from_xml(file_to_process):
    dataframe = pd.DataFrame(columns=["name", "height", "weight"])
    tree = ET.parse(file_to_process)
    root = tree.getroot()
    for person in root:
        name = person.find("name").text
        height = float(person.find("height").text)
        weight = float(person.find("weight").text)
        dataframe = pd.concat([dataframe, pd.DataFrame([{"name": name, "height": height, "weight": weight}])], ignore_index= True)
    return dataframe

def extract():
    extracted_data = pd.DataFrame(columns=["name", "height", "weight"])

    for csvfile in glob.glob("./source_files/*.csv"):
        if csvfile != target_file:
            extracted_data = pd.concat([extracted_data, extract_from_csv(csvfile)], ignore_index=True)

    for jsonfile in glob.glob("./source_files/*.json"):
        extracted_data = pd.concat([extracted_data, extract_from_json(jsonfile)], ignore_index=True)
    
    for xmlfile in glob.glob("./source_files/*.xml"):
        extracted_data = pd.concat([extracted_data, extract_from_xml(xmlfile)], ignore_index=True)

    return extracted_data


# Transform function

def transform(data):
    # height unit from inches to metre
    data["height"] = round(data.height * 0.0254, 2)

    # weight unit from pounds to kilograms
    data["weight"] = round(data.weight * 0.45359237, 2)

    return data


#load function
def load_data(destination_file, data):
    data.to_csv(destination_file)

# log function
def log_progress(message):
    timestamp_format = r'%Y-%h-%d-%H:%M:%S'
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)
    with open(log_file, "a") as lf:
        lf.write(timestamp + ',' + message + '\n')

if __name__ == "__main__":
    main()