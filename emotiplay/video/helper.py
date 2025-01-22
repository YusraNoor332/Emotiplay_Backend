from langchain_huggingface import HuggingFaceEndpoint
from django.conf import settings

secret_key = settings.HUGGING_FACE_API_KEY


repo_id = "mistralai/Mistral-7B-Instruct-v0.2"


llm = HuggingFaceEndpoint(
    repo_id=repo_id, temperature=0.7, huggingfacehub_api_token=secret_key
)


def invoke_model(prompt):
    """Function to send prompt to the Hugging Face model and get response"""
    try:
        response = llm.invoke(prompt)
        print(f"Model response: {response}")  # Print the response to the command line
        return response
    except Exception as e:
        error_message = f"Error: {str(e)}"
        print(error_message)  # Print error message if there's an exception
        return error_message
