from django.test import TestCase, Client
import json
from django.urls import reverse
from rest_framework import status

from .serializer import AudioBookSerializer, SongSerializer, PodcastSerializer
from .models import Song, AudioBook, Podcast
import ast

# object of class Cilent
client = Client()


class AudioBookTestcase(TestCase):
    """AudioBookTestcase is class for writing the
       testcases for audio_book"""

    def setUp(self):
        """on hitting this file firstly the setup methos will call"""

        # create the audio book entries in the database
        AudioBook.objects.create(
            duration=1, title_of_the_audiobook="hello",
            author_of_audiobook='Gradane',
            narrator='Brown')

        AudioBook.objects.create(
            duration=1, title_of_the_audiobook="hello",
            author_of_audiobook='Labrador',
            narrator='Black')

        AudioBook.objects.create(
            duration=1, title_of_the_audiobook="hello",
            author_of_audiobook='Labrador',
            narrator='Brown')

    def test_create_audio_book(self):
        """here post request have its own
            database which automatically vanish"""
        # data needs to be inserted
        data = {"duration": 1, "title_of_the_audiobook": "hope",
                "author_of_audiobook": "Mayank", "narrator": "Arya"}
        # convert the data into json
        data = json.dumps(data)
        response = client.post("/audio/audio_book/", data,
                               content_type="application/json")
        # assert for status code 201
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_bad_request_audio_book(self):
        """here we have some required field missing that is duration
            it is Bad request error"""
        # mock data
        data = {"title_of_the_audiobook": "hope",
                "author_of_audiobook": "Mayank", "narrator": "Arya"}
        data = json.dumps(data)
        response = client.post("/audio/audio_book/", data,
                               content_type="application/json")
        # check for 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bad_request_for_invalid_url(self):
        """check for invalid url"""

        data = {"duration": 1, "title_of_the_audiobook": "hope",
                "author_of_audiobook": "Mayank", "narrator": "Arya"}
        data = json.dumps(data)
        response = client.post("/audio/auuah/", data,
                               content_type="application/json")
        # 400 bad request error by passing wrong view key word argument
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_404_not_found_error(self):
        """check for 404 Not Found error"""
        data = {"duration": 1, "title_of_the_audiobook": "hope",
                "author_of_audiobook": "Mayank", "narrator": "Arya"}
        data = json.dumps(data)
        # the url which is not exists
        response = client.post("/audio/", data,
                               content_type="application/json")
        # assert for 404 Not Found error
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_audio_book(self):
        """test for get the data which is already created in setUp method"""
        response = client.get(reverse('audiofile',
                              kwargs={'type_of_audio': 'audio_book'}))
        audio_books = AudioBook.objects.all()
        serializer = AudioBookSerializer(audio_books, many=True)
        # match the serializer response with api response
        self.assertEqual(response.data, serializer.data)

    def test_get_audio_book_by_id(self):
        """test for retrieve operation"""
        response = client.get(reverse('audiofile_by_id',
                              kwargs={'type_of_audio': 'audio_book', 'pk': 1}))
        # find instance by id
        audio_book = AudioBook.objects.filter(id=1).last()
        serializer = AudioBookSerializer(audio_book)
        # instance data
        self.assertEqual(response.data, serializer.data)

    def test_get_audio_book_by_id_error_invalid_pk(self):
        """test for Invalid pk"""
        # Invalid pk
        pk = "dlknnvkdnlvd"
        type_of_audio = "audio_book"
        # response by id
        response = client.get(reverse('audiofile_by_id',
                              kwargs={
                               'type_of_audio': "{}".format(type_of_audio),
                               'pk': "{}".format(pk)
                               }))
        byte_str = response.content
        dict_str = byte_str.decode("UTF-8")
        # convert the byte code to the dict
        response_dict = ast.literal_eval(dict_str)
        error_str = response_dict.get('error')
        expected_output = "Invalid pk/id {}".format(pk)
        # comapare the status
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # comapare the error message
        self.assertEqual(error_str, expected_output)

    def test_get_audio_book_by_id_error_invalid_type_of_audio(self):
        """test for invalid type of audio"""
        pk = 1
        # Invalid audio name
        type_of_audio = "audio"
        response = client.get(reverse('audiofile_by_id',
                              kwargs={
                               'type_of_audio': "{}".format(type_of_audio),
                               'pk': "{}".format(pk)
                               }))
        byte_str = response.content
        dict_str = byte_str.decode("UTF-8")
        response_dict = ast.literal_eval(dict_str)
        error_str = response_dict.get('error')
        expected_output = "Invalid type of audio {} Hint: choose from ['song', 'audio_book', 'podcast']".format(type_of_audio)
        # comapre the status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # compare the error message
        self.assertEqual(error_str, expected_output)

    def test_update_audio_book(self):
        """update the already created"""
        pk = 1
        type_of_audio = "audio_book"
        data = {"duration": 2}
        data = json.dumps(data)
        # response
        response = client.put(reverse('audiofile_by_id',
                              kwargs={
                               'type_of_audio': "{}".format(type_of_audio),
                               'pk': "{}".format(pk)
                               }), data=data, content_type="application/json")
        # comapre the error message
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_audio_book(self):
        """delete the particular entry from db"""
        pk = 1
        type_of_audio = "audio_book"
        response = client.delete(reverse('audiofile_by_id',
                                 kwargs={
                                  'type_of_audio': "{}".format(type_of_audio),
                                  'pk': "{}".format(pk)
                                   }))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # after deleting we want to get it
        response_get_already_deleted_id = client.get(
            reverse('audiofile_by_id',
                    kwargs={
                     'type_of_audio': "{}".format(type_of_audio),
                     'pk': "{}".format(pk)
                     }))
        self.assertEqual(response_get_already_deleted_id.status_code,
                         status.HTTP_404_NOT_FOUND)


class PodcastTestcase(TestCase):
    """PodcastTestcase is class for writing the
       testcases for podcast"""

    def setUp(self):
        """on hitting this file firstly the setup methos will call"""

        # create the podcast entries in the database
        Podcast.objects.create(
            duration=1, name_of_podcast="hello", host='Gradane',
            participants='Arya, Kumar, Bhawna')
        Podcast.objects.create(
            duration=1, name_of_podcast="hello", host='Labrador',
            participants='Arya, Kumar, Bhawna')
        Podcast.objects.create(
            duration=1, name_of_podcast="hello", host='Labrador',
            participants='Arya, Kumar, Bhawna')

    def test_create_podcast(self):
        """here post request have its own
            database which automatically vanish"""
        # data to be created
        data = {"duration": 1, "name_of_podcast": "hope", "host": "Mayank",
                "participants": "Arya, Kumar, Bhawna"}
        # convert the data into json
        data = json.dumps(data)
        response = client.post("/audio/podcast/", data,
                               content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_bad_request_podcast(self):
        """here we have some required field missing that is duration
            it is Bad request error"""
        # mock data
        data = {"name_of_podcast": "hope", "host": "Mayank", "narrator": "Arya, Kumar, Bhawna"}
        data = json.dumps(data)
        response = client.post("/audio/podcast/", data,
                               content_type="application/json")
        # check for 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_podcast(self):
        """test for get the data which is already created in setUp method"""
        response = client.get(reverse('audiofile',
                              kwargs={'type_of_audio': 'podcast'}))
        # database query
        podcasts = Podcast.objects.all()
        serializer = PodcastSerializer(podcasts, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_get_podcast_by_id(self):
        """test for get the data by id which is already
            created in setUp method"""
        response = client.get(reverse('audiofile_by_id',
                              kwargs={'type_of_audio': 'podcast', 'pk': 1}))
        podcast = Podcast.objects.filter(id=1).last()
        serializer = PodcastSerializer(podcast)
        # compare the data
        self.assertEqual(response.data, serializer.data)

    def test_get_podcast_by_id_error_invalid_pk(self):
        """test for Invalid pk"""
        # Invalid pk
        pk = "dlknnvkdnlvd"
        type_of_audio = "podcast"
        # response by id
        response = client.get(reverse('audiofile_by_id',
                              kwargs={
                               'type_of_audio': "{}".format(type_of_audio),
                               'pk': "{}".format(pk)
                               }))
        byte_str = response.content
        dict_str = byte_str.decode("UTF-8")
        # convert the byte code to the dict
        response_dict = ast.literal_eval(dict_str)
        error_str = response_dict.get('error')
        expected_output = "Invalid pk/id {}".format(pk)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(error_str, expected_output)

    def test_get_podcast_by_id_error_invalid_type_of_audio(self):
        """test for invalid type of audio"""
        pk = 1
        # Invalid audio name
        type_of_audio = "audio"
        response = client.get(reverse('audiofile_by_id',
                              kwargs={
                               'type_of_audio': "{}".format(type_of_audio),
                               'pk': "{}".format(pk)
                               }))
        byte_str = response.content
        dict_str = byte_str.decode("UTF-8")
        response_dict = ast.literal_eval(dict_str)
        error_str = response_dict.get('error')
        expected_output = "Invalid type of audio {} Hint: choose from ['song', 'audio_book', 'podcast']".format(type_of_audio)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(error_str, expected_output)

    def test_update_podcast(self):
        """update the already created"""
        pk = 1
        type_of_audio = "podcast"
        data = {"duration": 2}
        data = json.dumps(data)
        response = client.put(reverse('audiofile_by_id',
                              kwargs={
                               'type_of_audio': "{}".format(type_of_audio),
                               'pk': "{}".format(pk)
                               }), data=data, content_type="application/json")
        # comapre the error message
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_podcast(self):
        """delete the particular entry from db"""
        pk = 1
        type_of_audio = "podcast"
        response = client.delete(reverse('audiofile_by_id',
                                 kwargs={
                                  'type_of_audio': "{}".format(type_of_audio),
                                  'pk': "{}".format(pk)
                               }))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_get_already_deleted_id = client.get(
            reverse('audiofile_by_id',
                    kwargs={
                     'type_of_audio': "{}".format(type_of_audio),
                     'pk': "{}".format(pk)
                     }))
        self.assertEqual(response_get_already_deleted_id.status_code,
                         status.HTTP_404_NOT_FOUND)


class SongTestcase(TestCase):

    def setUp(self):
        """on hitting this file firstly the setup methos will call"""

        # create the song entries in the database
        Song.objects.create(
            duration=1, name_of_song="hello")
        Song.objects.create(
            duration=1, name_of_song="hello")
        Song.objects.create(
            duration=1, name_of_song="hello")

    def test_create_song(self):
        """here post request have its own
            database which automatically vanish"""
        # data needs to be inserted
        data = {"duration": 1, "name_of_song": "hope"}
        # convert the data into json
        data = json.dumps(data)
        response = client.post("/audio/song/", data,
                               content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_bad_request_song(self):
        """here we have some required field missing that is duration
            it is Bad request error"""
        # mock data
        data = {"name_of_song": "hope"}
        data = json.dumps(data)
        response = client.post("/audio/song/", data,
                               content_type="application/json")
        # check for 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_song(self):
        """test for get the data which is already created in setUp method"""
        response = client.get(reverse('audiofile',
                              kwargs={'type_of_audio': 'song'}))
        songs = Song.objects.all()
        serializer = SongSerializer(songs, many=True)
        # comapare the serializer data
        self.assertEqual(response.data, serializer.data)

    def test_get_song_by_id(self):
        """test for get the data by id which is already
           created in setUp method"""
        response = client.get(reverse('audiofile_by_id',
                              kwargs={'type_of_audio': 'song', 'pk': 1}))
        song = Song.objects.filter(id=1).last()
        serializer = SongSerializer(song)
        self.assertEqual(response.data, serializer.data)

    def test_get_song_by_id_error_invalid_pk(self):
        """test for Invalid pk"""
        # Invalid pk
        pk = "njjj"
        type_of_audio = "song"
        # response by id
        response = client.get(reverse('audiofile_by_id',
                              kwargs={
                               'type_of_audio': "{}".format(type_of_audio),
                               'pk': "{}".format(pk)
                               }))
        byte_str = response.content
        dict_str = byte_str.decode("UTF-8")
        response_dict = ast.literal_eval(dict_str)
        # convert the byte code to the dict
        error_str = response_dict.get('error')
        expected_output = "Invalid pk/id {}".format(pk)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(error_str, expected_output)

    def test_get_song_by_id_error_invalid_type_of_audio(self):
        """test for invalid type of audio"""
        pk = 1
        # Invalid audio name
        type_of_audio = "lkdnkldc"
        response = client.get(reverse('audiofile_by_id',
                              kwargs={
                               'type_of_audio': "{}".format(type_of_audio),
                               'pk': "{}".format(pk)
                               }))
        byte_str = response.content
        dict_str = byte_str.decode("UTF-8")
        response_dict = ast.literal_eval(dict_str)
        error_str = response_dict.get('error')
        expected_output = "Invalid type of audio {} Hint: choose from ['song', 'audio_book', 'podcast']".format(type_of_audio)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(error_str, expected_output)

    def test_update_song(self):
        """update the already created"""
        pk = 1
        type_of_audio = "song"
        data = {"duration": 2}
        data = json.dumps(data)
        response = client.put(reverse('audiofile_by_id',
                              kwargs={
                               'type_of_audio': "{}".format(type_of_audio),
                               'pk': "{}".format(pk)
                               }), data=data, content_type="application/json")
        # comapre the error message
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_song(self):
        """delete the particular entry from db"""
        pk = 1
        type_of_audio = "song"
        response = client.delete(reverse('audiofile_by_id',
                                 kwargs={
                                  'type_of_audio': "{}".format(type_of_audio),
                                  'pk': "{}".format(pk)
                                 }))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_get_already_deleted_id = client.get(
            reverse('audiofile_by_id',
                    kwargs={
                     'type_of_audio': "{}".format(type_of_audio),
                     'pk': "{}".format(pk)
                     }))

        self.assertEqual(response_get_already_deleted_id.status_code,
                         status.HTTP_404_NOT_FOUND)
