from django.http import JsonResponse
from rest_framework import status

class VerifyView(object):
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        type_of_audio = view_kwargs.get('type_of_audio')
        type_of_audio = type_of_audio.lower()
        type_of_audio_options = ["song", "audio_book", "podcast"]

        if type_of_audio not in type_of_audio_options:
            # if type of audio is not in valid choice then it throw error
            return JsonResponse({"error": "Invalid type of audio {0} Hint: choose from {1}".format(type_of_audio, type_of_audio_options)}, status=status.HTTP_400_BAD_REQUEST)

        if view_kwargs.get('pk'):
            # if pk is not integer then it throws Invalid pk/id error
            pk = view_kwargs.get('pk')
            if not pk.isdigit():
                return JsonResponse({"error": "Invalid pk/id {}".format(pk)}, status=status.HTTP_400_BAD_REQUEST)
        return None