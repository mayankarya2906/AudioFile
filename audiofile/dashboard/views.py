from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializer import AudioBookSerializer, SongSerializer, PodcastSerializer
from rest_framework.decorators import action
from .models import Song, AudioBook, Podcast


class AudioFileViewset(viewsets.ViewSet):

    # helper method of AudioFileViewset class
    def get_model_serailizer(self, type_of_audio):
        """return type <serailizer class>
        params: type_of_audio"""

        # if song then SongSerializer will return
        # similarly for both audio type
        mapping_of_serializer = {
            'song': SongSerializer,
            'audio_book': AudioBookSerializer,
            'podcast': PodcastSerializer
        }
        model_serializer = mapping_of_serializer.get(type_of_audio)
        return model_serializer

    def get_model_name(self, type_of_audio):
        """"return type <model class>
        params: type_of_audio"""

        # if song then Song will return
        # similarly for both audio type
        mapping_of_instance = {
            'song': Song,
            'audio_book': AudioBook,
            'podcast': Podcast,
        }
        model_name = mapping_of_instance.get(type_of_audio)
        return model_name
    
    def get_instance(self, model_name, pk):
        """"return type <model instance>
        params: model_name
        params: pk"""
        instance = get_object_or_404(model_name, id=pk)
        return instance

    def create(self, request, format=None, **kwargs):
        """creates the new entry in the database as row"""
        request_data = request.data
        # find the type_of_audio and lower it
        type_of_audio = self.kwargs.get('type_of_audio').lower()
        # find model seriaizer class
        model_serializer_class = self.get_model_serailizer(type_of_audio)
        model_serializer = model_serializer_class(data=request_data)
        # check for validation
        model_serializer.is_valid(raise_exception=True)
        # save the instance
        model_serializer.save(data=request_data)
        #show the data
        response_data = model_serializer.data
        return Response(response_data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, format=None, **kwargs):
        """update existing row of the database"""
        # find the type_of_audio and lower it
        type_of_audio = self.kwargs.get('type_of_audio').lower()
        request_data = request.data
        model_name = self.get_model_name(type_of_audio)
        # find instance
        instance = self.get_instance(model_name=model_name, pk=pk)
        model_serializer_class = self.get_model_serailizer(type_of_audio)
        # send instance to serializer
        model_serializer = model_serializer_class(instance=instance, data=request_data, partial=True)
        # raise exception in case of error
        model_serializer.is_valid(raise_exception=True)
        model_serializer.save(data=request.data)
        # show data as response
        response = model_serializer.data
        return Response(response, status=status.HTTP_200_OK)
    
    def delete(self, request, pk=None, format=None, **kwargs):
        """delete the instance from database permanently"""
        type_of_audio = self.kwargs.get('type_of_audio').lower()
        model_name = self.get_model_name(type_of_audio)
        # find instance
        instance = self.get_instance(model_name=model_name, pk=pk)
        # delete it
        instance.delete()
        return Response({"msg": "sucessfully deleted"}, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None, format=None, **kwargs):
        """get by id/pk"""
        type_of_audio = self.kwargs.get('type_of_audio').lower()
        model_name = self.get_model_name(type_of_audio)
        # find instance
        instance = self.get_instance(model_name=model_name, pk=pk)
        model_serializer_class = self.get_model_serailizer(type_of_audio)
        model_serializer = model_serializer_class(instance=instance)
        response = model_serializer.data
        return Response(response, status=status.HTTP_200_OK)

    def list(self, request, format=None, **kwargs):
        """get all the instance"""
        type_of_audio = self.kwargs.get('type_of_audio').lower()
        model_name = self.get_model_name(type_of_audio)
        model_serializer_class = self.get_model_serailizer(type_of_audio)
        # find queryset of one type of audio pass as view keyword argument
        queryset = model_name.objects.all()
        model_serializer = model_serializer_class(queryset, many=True)
        # show the serialized data
        response = model_serializer.data
        return Response(response, status=status.HTTP_200_OK)
