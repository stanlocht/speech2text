import os
import time
from google.cloud import storage
from google.cloud import speech_v1
import subprocess


os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="credentials.json"

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)
    print()
    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )
    
def long_running_recognize(storage_uri, channels, sample_rate):

    client = speech_v1.SpeechClient()

    config = {
        "language_code": "nl-NL",
        "sample_rate_hertz": int(sample_rate),
        "encoding": speech_v1.RecognitionConfig.AudioEncoding.LINEAR16,
        "audio_channel_count": int(channels),
        "enable_word_time_offsets": True,
        "model": "default",
        "enable_automatic_punctuation":True
    }
    audio = {"uri": storage_uri}

    operation = client.long_running_recognize(request={"config":config, "audio":audio})


    # Make sure progress is printed:
    def callback(operation_future):
        result = operation_future.result()
        progress = operation.metadata.progress_percent

    operation.add_done_callback(callback)

    progress = 0

    print('Progress: 0%')
    while progress < 100:
        try:
            if operation.metadata.progress_percent != progress:
                print('Progress: {}%'.format(operation.metadata.progress_percent))
                progress = operation.metadata.progress_percent
        except:
            pass
        finally:
            time.sleep(5)


    print('Transcription Done!')        
    response = operation.result()
    return response



def main(BUCKET_NAME = '', audio_filename = '', channels = 0 , sample_rate = 0,)
    blob_name = f"audios/{audio_filename}"
    upload_blob(BUCKET_NAME, audio_filename, blob_name)
    gcs_uri = f"gs://{BUCKET_NAME}/{blob_name}"

    response=long_running_recognize(gcs_uri, channels, sample_rate)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(u"Transcript: {}".format(result.alternatives[0].transcript))
        print("Confidence: {}".format(result.alternatives[0].confidence))

    return result


if __name__ == "__main__":
    audio_filename = ''
    BUCKET_NAME = ''
    channels = 
    sample_rate = 

    response=long_running_recognize(gcs_uri, channels, sample_rate)

    main(BUCKET_NAME, audio_filename, channels, sample_rate)
