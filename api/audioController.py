from flask import Response, request, jsonify
from flask_restful import Resource
from models.audioModel import Song, Podcast, Audiobook
from middleware.errors import invalid_request
from middleware.cloud import cloud_save
from werkzeug.utils import secure_filename
import os


up_config = "uploads"

class AudioFileDatabase:

    def __init__(self):

        self.audiofile = {
            'song': Song,
            'podcast': Podcast,
            'audiobook': Audiobook
        }
        

    def database(self):
        return self.audiofile



class AudioFileAPI(Resource):

    def __init__(self):
        self.database = AudioFileDatabase().database()
        self.allowed_extensions = set(['mp3'])



    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.allowed_extensions



    def post(self) -> Response:

        """to upload multiple files, try: request.files.getlist('file[]')"""

        if 'audioFile' not in request.files:
            return invalid_request

        else:
            
            audioFile = request.files['audioFile']

            if audioFile.filename == '':

                return invalid_request

            else:

                if audioFile and self.allowed_file(audioFile.filename):

                    filename = secure_filename(audioFile.filename)

                    audioFile.save(os.path.join(up_config, filename))

                    save_audio = cloud_save(audioFile)

                    if save_audio:

                        response_data = self.sortAudioFile(request.form, save_audio)
                        
                        if response_data['result']:

                            response = jsonify(response_data['result'])

                            response.status_code = 200

                            return response

                        else:
                            error = response_data['error']

                            if error.__class__.__name__ == 'ValidationError':

                                return invalid_request()

                            else:

                                return Response(status=500)

                        
                    
                    else:
                        return Response(status=500)



    def sortAudioFile(self, formdata, audioFileUrl):
        audioFileType = formdata['audioFileType']

        audioFileMetadata = formdata.to_dict()
        del audioFileMetadata['audioFileType']
        audioFileMetadata['url'] = audioFileUrl

        db = self.database[audioFileType]
        
        if audioFileType == 'song':
            try:
                post_data = db(**audioFileMetadata).save()
                result = {'id': str(post_data.id)}
                response = {"result": result}
                
                return response
            
            except Exception as error:
                
                error = {"error": error}
                return error

                
        elif audioFileType == 'podcast':
            try:
                post_data = db(**audioFileMetadata).save()
                result = {'id': str(post_data.id)}
                response = {"result": result}
                
                return response
            
            except Exception as error:
                
                error = {"error": error}
                return error

        elif audioFileType == 'audiobook':
            try:
                post_data = db(**audioFileMetadata).save()
                result = {'id': str(post_data.id)}
                response = {"result": result}
                
                return response
            
            except Exception as error:
                
                error = {"error": error}
                return error

        else:
            return invalid_request()
        



class AudioFileEditAPI(Resource):

    def __init__(self):
        self.database = AudioFileDatabase().database()


    def get(self, audioFileType: str, audioFileID: str = None) -> Response:


        try:
            db = self.database[audioFileType]
            
            if audioFileID is not None:
                
                data = db.objects.get(id=audioFileID)
                response = jsonify({'data': data})
                response.status_code = 200
                return response

            else:

                data = db.objects()
                response = jsonify({'data': data})
                response.status_code = 200
                return response

        except:
            return Response(status=500)

    

    def put(self, audioFileType: str , audioFileID: str) -> Response:
        """This method can only edit the audio file metadata, it cannot change the media file"""
        db = self.database[audioFileType]
        audioFileMetadata = request.get_json()['audioFileMetadata']

        try:
            data = db.objects(id=audioFileID).update(**audioFileMetadata)
            response = jsonify(({'result': 'audio file updated'}))
            response.status_code = 200
            return response
        

        except Exception as error:
            if error.__class__.__name__ == 'ValidationError':
                return invalid_request()
            else:
                return Response(status=500)




    def delete(self, audioFileType: str = None, audioFileID: str = None) -> Response:
        db = self.database[audioFileType]
        try:
            data = db.objects(id=audioFileID).delete()
            response = jsonify({'result': 'audio file deleted'})
            response.status_code = 200
            return response
        
        except:
            return invalid_request()
