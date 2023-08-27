import io
import streamlit as st
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
import base64
import wave

from pydub import AudioSegment


class Workflow:
    text_to_text_workflow = 'text-to-text'
    image_to_text_workflow = 'image-to-text'
    image_to_tags_workflow = 'image-to-tags'
    text_to_audio_workflow = 'text-to-audio'


@st.cache_data
def get_credentials():
    ##############################################################################
    # In this section, we set the user authentication, app ID, workflow ID, and
    # image URL. Change these strings to run your own example.
    ##############################################################################
    user_id = 'sdragan15'
    pat = '73028d3a4be24e18a7fdad1320333fb0'
    app_id = 'cool_app'
    return user_id, pat, app_id


def retrieve_clarifai_stub():
    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)
    return stub


@st.cache_data
def clarify_image_description(image: bytes) -> str:
    user_id, pat, app_id = get_credentials()

    user_data_object = resources_pb2.UserAppIDSet(user_id=user_id, app_id=app_id)

    stub = retrieve_clarifai_stub()
    post_workflow_results_response = stub.PostWorkflowResults(
        service_pb2.PostWorkflowResultsRequest(
            user_app_id=user_data_object,
            workflow_id=Workflow.image_to_text_workflow,
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        image=resources_pb2.Image(
                            base64=image
                        )
                    )
                )
            ]
        ),
        metadata=(('authorization', 'Key ' + pat),)
    )

    if post_workflow_results_response.status.code != status_code_pb2.SUCCESS:
        print(post_workflow_results_response.status)
        raise Exception("Post workflow results failed, status: " + post_workflow_results_response.status.description)

    results = post_workflow_results_response.results[0]
    outputs = results.outputs
    result = outputs[-1]
    return result.data.text.raw


@st.cache_data
def clarify_text_to_text(text: str, prompt: str) -> str:
    user_id, pat, app_id = get_credentials()
    user_data_object = resources_pb2.UserAppIDSet(user_id=user_id, app_id=app_id)

    stub = retrieve_clarifai_stub()
    post_workflow_results_response = stub.PostWorkflowResults(
        service_pb2.PostWorkflowResultsRequest(
            user_app_id=user_data_object,
            workflow_id=Workflow.text_to_text_workflow,
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        text=resources_pb2.Text(
                            raw="{} {}.".format(text, prompt)
                        )
                    )
                )
            ]
        ),
        metadata=(('authorization', 'Key ' + pat),)
    )

    if post_workflow_results_response.status.code != status_code_pb2.SUCCESS:
        print(post_workflow_results_response.status)
        raise Exception("Post workflow results failed, status: " + post_workflow_results_response.status.description)

    results = post_workflow_results_response.results[0]
    outputs = results.outputs
    result = outputs[-1]
    return result.data.text.raw


@st.cache_data
def clarify_image_to_hashtags(image: bytes):
    user_id, pat, app_id = get_credentials()

    user_data_object = resources_pb2.UserAppIDSet(user_id=user_id, app_id=app_id)

    stub = retrieve_clarifai_stub()

    post_workflow_results_response = stub.PostWorkflowResults(
        service_pb2.PostWorkflowResultsRequest(
            user_app_id=user_data_object,
            workflow_id=Workflow.image_to_tags_workflow,
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        image=resources_pb2.Image(
                            base64=image
                        )
                    )
                )
            ]
        ),
        metadata=(('authorization', 'Key ' + pat),)
    )
    if post_workflow_results_response.status.code != status_code_pb2.SUCCESS:
        print(post_workflow_results_response.status)
        raise Exception("Post workflow results failed, status: " + post_workflow_results_response.status.description)

    # We'll get one WorkflowResult for each input we used above. Because of one input, we have here one WorkflowResult
    results = post_workflow_results_response.results[0]

    tags = []
    # Each model we have in the workflow will produce one output.
    for output in results.outputs:
        model = output.model

        for concept in output.data.concepts:
            print("	%s %.2f" % (concept.name, concept.value))
            tags.append(concept.name)

    tags_text = ''
    for i in tags:
        tags_text = tags_text + '#' + i.replace(' ', '_') + ' '

    tags_text = tags_text[:-1]
    return tags_text


@st.cache_data
def clarify_text_to_audio(text):
    ######################################################################################################
    # In this section, we set the user authentication, user and app ID, model details, and the URL of 
    # the text we want as an input. Change these strings to run your own example.
    ######################################################################################################

    # Your PAT (Personal Access Token) can be found in the portal under Authentification
    PAT = '73028d3a4be24e18a7fdad1320333fb0'
    # Specify the correct user_id/app_id pairings
    # Since you're making inferences outside your app's scope
    USER_ID = 'sdragan15'
    APP_ID = 'cool_app'
    # Change these to whatever model and text URL you want to use
    WORKFLOW_ID = 'text-to-audio'
    TEXT_FILE_URL = 'https://samples.clarifai.com/negative_sentence_12.txt'

    ############################################################################
    # YOU DO NOT NEED TO CHANGE ANYTHING BELOW THIS LINE TO RUN THIS EXAMPLE
    ############################################################################

    from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
    from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
    from clarifai_grpc.grpc.api.status import status_code_pb2

    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)

    metadata = (('authorization', 'Key ' + PAT),)

    userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)

    post_workflow_results_response = stub.PostWorkflowResults(
        service_pb2.PostWorkflowResultsRequest(
            user_app_id=userDataObject,
            workflow_id=WORKFLOW_ID,
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        text=resources_pb2.Text(
                            raw=text
                        )
                    )
                )
            ]
        ),
        metadata=metadata
    )
    if post_workflow_results_response.status.code != status_code_pb2.SUCCESS:
        print(post_workflow_results_response.status)
        raise Exception("Post workflow results failed, status: " + post_workflow_results_response.status.description)

    # We'll get one WorkflowResult for each input we used above. Because of one input, we have here one WorkflowResult
    results = post_workflow_results_response.results[0]

    # Each model we have in the workflow will produce one output.
    for output in results.outputs:
        model = output.model

        print("Predicted concepts for the model `%s`" % model.id)
        for concept in output.data.concepts:
            print("	%s %.2f" % (concept.name, concept.value))

    # Uncomment this line to print the full Response JSON

    outputs = results.outputs
    last = outputs[-1]

    return last.data.audio.base64


def decode_base64_to_audio_stream(base64_string):
    audio_data = base64.b64decode(base64_string)
    return io.BytesIO(audio_data)


def merge_audio_streams(audio_streams: list[io.BytesIO], output_format="wav"):
    combined_audio = AudioSegment.empty()
    for audio_stream in audio_streams:
        audio_stream.seek(0)
        audio = AudioSegment.from_wav(audio_stream)
        combined_audio += audio

    merged_audio_stream = io.BytesIO()
    combined_audio.export(merged_audio_stream, format=output_format)
    return merged_audio_stream


def clarify_story_to_audio(story: str):
    sentences = story.split('.')
    base64_segments = []
    for sentence in sentences:
        retries = 3
        count = 0
        while count < retries:
            try:
                base64_segments.append(clarify_text_to_audio(sentence))
                break;
            except Exception as e:
                count += 1
                print(e)
                pass

    audio_streams = [io.BytesIO(data) for data in base64_segments]

    merged_audio_stream = merge_audio_streams(audio_streams)
    return merged_audio_stream


def clarify_image_to_story(image: bytes, user_input: str):
    image_description = clarify_image_description(image)
    result = clarify_text_to_text(image_description, "Create a short story. {}".format(user_input)) + " "

    last_dot_index = result.rfind(".") + 1
    result = result[:last_dot_index]

    return result


def get_data_from_clarify(user_input: str, image: bytes) -> str:
    audio = None
    story = clarify_image_to_story(image, user_input)
    if story is None:
        st.write("Mighty AI was not inspired to write a story for this image with the particular parameters. Maybe try something else?")
    elif story.strip() == "":
        st.write("Mighty AI was not inspired to write a story for this image with the particular parameters. Maybe try something else?")
    else:
        audio = clarify_story_to_audio(story)

    tags = clarify_image_to_hashtags(image)
    return story, tags, audio
