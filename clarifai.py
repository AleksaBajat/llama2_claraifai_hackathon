import streamlit as st

@st.cache_data
def get_credentials():
    ##############################################################################
    # In this section, we set the user authentication, app ID, workflow ID, and
    # image URL. Change these strings to run your own example.
    ##############################################################################

    user_id = 'sdragan15'
    # Your PAT (Personal Access Token)
    pat = '73028d3a4be24e18a7fdad1320333fb0'
    app_id = 'cool_app'
    workflow_id = 'workflow-306cec'
    workflow_tags_id = 'workflow-f33888'
    image_url = 'https://samples.clarifai.com/metro-north.jpg'
    return user_id, pat, app_id, workflow_id, workflow_tags_id, image_url


@st.cache_data
def get_data_from_clarify(text: str, image: bytes) -> str:

    ##########################################################################
    # YOU DO NOT NEED TO CHANGE ANYTHING BELOW THIS LINE TO RUN THIS EXAMPLE
    ##########################################################################

    from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
    from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
    from clarifai_grpc.grpc.api.status import status_code_pb2

    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)

    user_id, pat, app_id, workflow_id, workflow_tags_id, image_url = get_credentials()

    metadata = (('authorization', 'Key ' + pat),)

    user_data_object = resources_pb2.UserAppIDSet(user_id=user_id,
                                                app_id=app_id)  # The userDataObject is required when using a PAT

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

        for concept in output.data.concepts:
            print("	%s %.2f" % (concept.name, concept.value))

    # Uncomment this line to print the full Response JSON
    # print(results.status)

    outputs = results.outputs
    result = outputs[-1]    



    post_workflow_results_response = stub.PostWorkflowResults(
        service_pb2.PostWorkflowResultsRequest(
            user_app_id=user_data_object,  
            workflow_id=workflow_tags_id,
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
        metadata=metadata
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



    return result.data.text.raw, tags
