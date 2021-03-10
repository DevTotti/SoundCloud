from flask import jsonify
import cloudinary
import cloudinary.uploader 
import cloudinary.api as cloudAPI
from dotenv import load_dotenv

import os
load_dotenv()




cloud_name = os.environ["CLOUD_NAME"]
cloud_api_key = os.environ["API_KEY"]
cloud_api_secret = os.environ["API_SECRET"]
cloud_folder = os.environ["CLOUD_FOLDER"]


def connectCloudinary():
    
    try:
        cloudinary.config(
            cloud_name = cloud_name,
            api_key = cloud_api_key,
            api_secret = cloud_api_secret
        )

        response = jsonify({"result":200})
        response.status_code == 200
        return response
        
    
    except:
        response = jsonify({"result": 500})
        response.status_code == 400
        return response



def cloud_save(audioFile):
    audioFile = 'uploads/'+audioFile.filename
    check_connection = connectCloudinary()
    if check_connection.status_code == 200:
        
        try:
            save_file = cloudinary.uploader.upload(
                audioFile,
                resource_type = "video",
                folder = "AudioFiles"
            )

            file_url = save_file['url']
            
            return file_url


        except Exception as error:
            print(error)
            

    else:
        return check_connection
