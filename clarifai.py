import streamlit as st
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2


@st.cache_data
def get_credentials():
    ##############################################################################
    # In this section, we set the user authentication, app ID, workflow ID, and
    # image URL. Change these strings to run your own example.
    ##############################################################################
    user_id = 'sdragan15'
    pat = '73028d3a4be24e18a7fdad1320333fb0'
    app_id = 'cool_app'
    workflow_id = 'workflow-306cec'
    return user_id, pat, app_id, workflow_id


def retrieve_clarifai_stub():
    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)
    return stub


def clarify_image_to_story(text: str, image: bytes) -> str:
    user_id, pat, app_id, workflow_id = get_credentials()

    user_data_object = resources_pb2.UserAppIDSet(user_id=user_id,
                                                  app_id=app_id)

    stub = retrieve_clarifai_stub()
    post_workflow_results_response = stub.PostWorkflowResults(
        service_pb2.PostWorkflowResultsRequest(
            user_app_id=user_data_object,
            workflow_id=workflow_id,
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
def get_data_from_clarify(text: str, image: bytes) -> str:
    image_story = clarify_image_to_story(text, image)
    return image_story
