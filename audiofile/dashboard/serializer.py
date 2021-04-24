from rest_framework import serializers
from .models import AudioBook, Song, Podcast
from datetime import datetime

# helping function
def pop_out_extra_fields(request_data, request_keys, type_of_audio):
    """"return type <dict>
    params: request_data
    params: request_keys
    params: type_of_audio"""

    # every type of audio have different fields
    mapping_of_fields =  {
        'audio_book': ['title_of_the_audiobook', 'author_of_audiobook', 'narrator', 'duration', 'upload_time'],
        'song': ['name_of_song', 'duration', 'upload_time'],
        'podcast': ['name_of_podcast', 'host', 'participants', 'duration', 'upload_time'],
        }
    # find the field list
    fields = mapping_of_fields.get(type_of_audio)

    # pop out the extra fields from the request data and return the relevant data
    [request_data.pop(key) for key in request_keys if key not in fields]
    return request_data


class AudioBookSerializer(serializers.ModelSerializer):
    """"serailizer for audio book (type of audio)"""

    def create(self, validated_data):
        """creates the new entry in the database as row"""
        # data needs to validate
        audio_book_data = validated_data["data"]
        # list of keys passed as request data
        audio_book_data_keys = list(audio_book_data.keys())
        # pop out irrevalant fields
        audio_book_data = pop_out_extra_fields(request_data=audio_book_data, request_keys=audio_book_data_keys, type_of_audio='audio_book')
        # create instance of audio book
        audio_book_instance = AudioBook.objects.create(**audio_book_data)
        return audio_book_instance

    def update(self, instance, validated_data):
        """"update the instance of the audio_book"""
        audio_book_data = validated_data["data"]
        audio_book_data_keys = list(audio_book_data.keys())
        audio_book_data = pop_out_extra_fields(request_data=audio_book_data, request_keys=audio_book_data_keys, type_of_audio='audio_book')
        # here we update the instance
        AudioBook.objects.filter(id=instance.id).update(**audio_book_data)
        return instance

    class Meta:
        model = AudioBook
        # all the fields
        fields = '__all__'

class PodcastSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        """creates the new entry in the database as row"""
        podcast_data = validated_data["data"]
        podcast_data_keys = list(podcast_data.keys())
        # pop out irrvalant fields
        podcast_data = pop_out_extra_fields(request_data=podcast_data, request_keys=podcast_data_keys, type_of_audio='podcast')
        # create new entry
        podcast_instance = Podcast.objects.create(**podcast_data)
        return podcast_instance
        
    def update(self, instance, validated_data):
        """"update the instance of the podcast"""
        podcast_data = validated_data["data"]
        podcast_data_keys = list(podcast_data.keys())
        podcast_data = pop_out_extra_fields(request_data=podcast_data, request_keys=podcast_data_keys, type_of_audio='podcast')
        Podcast.objects.filter(id=instance.id).update(**podcast_data)
        return instance

    class Meta:
        model = Podcast
        fields = '__all__'

class SongSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        """creates the new entry in the database as row"""
        song_data = validated_data["data"]
        song_data_keys = list(song_data.keys())
        song_data = pop_out_extra_fields(request_data=song_data, request_keys=song_data_keys, type_of_audio='song')
        song_instance = Song.objects.create(**song_data)
        return song_instance
    
    def update(self, instance, validated_data):
        """"update the instance of the song"""
        song_data = validated_data["data"]
        song_data_keys = list(song_data.keys())
        song_data = pop_out_extra_fields(request_data=song_data, request_keys=song_data_keys, type_of_audio='song')
        Song.objects.filter(id=instance.id).update(**song_data)
        return instance

    class Meta:
        model = Song
        fields = '__all__'
