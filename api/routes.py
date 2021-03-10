from flask_restful import Api
from api.audioController import AudioFileAPI, AudioFileEditAPI

def api_routes(api: Api):
    api.add_resource(AudioFileAPI, '/')
    api.add_resource(AudioFileEditAPI, "/media/<audioFileType>/", "/media/<audioFileType>/<audioFileID>")

    return api