"""Wrapper around Sagemaker InvokeEndpoint API."""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Mapping, Optional, Union

from ..wrapper_interfaces.model_wrapper import ModelWrapper
from omnibridge.model_entities.models_io.base_model_io import ModelIO
import boto3
import json


class ContentHandlerBase(ABC):
    """A handler class to transform ModelIO to a
    format that SageMaker endpoint expects. Similarily,
    the class also handles transforming output from the
    SageMaker endpoint to a ModelIO.
    """

    """
    Example:
        .. code-block:: python
            class ContentHandler(ContentHandlerBase):
                content_type = "application/json"
                accepts = "application/json"
                def transform_input(self, prompt: str, model_kwargs: Dict) -> bytes:
                    input_str = json.dumps({prompt: prompt, **model_kwargs})
                    return input_str.encode('utf-8')
                
                def transform_output(self, output: bytes) -> str:
                    response_json = json.loads(output.read().decode("utf-8"))
                    return response_json[0]["generated_text"]
    """

    content_type: Optional[str] = "text/plain"
    """The MIME type of the input data passed to endpoint"""

    accepts: Optional[str] = "text/plain"
    """The MIME type of the response data returned from endpoint"""

    @abstractmethod
    def transform_input(
        self, prompt: ModelIO, model_kwargs: Dict
    ) -> bytes:
        """Transforms the input to a format that model can accept
        as the request Body. Should return bytes or seekable file
        like object in the format specified in the content_type
        request header.
        """

    @abstractmethod
    def transform_output(self, output: bytes) -> ModelIO:
        """Transforms the output from the model to string that
        the LLM class expects.
        """

class ContentHandler(ContentHandlerBase):
    content_type = "application/json"
    accepts = "application/json"
    def transform_input(self, prompt: ModelIO, model_kwargs: Dict) -> bytes:
        input_str = json.dumps({prompt: prompt, **model_kwargs})
        return input_str.encode('utf-8')
    
    def transform_output(self, output: bytes) -> ModelIO:
        response_json = json.loads(output.read().decode("utf-8"))
        return response_json[0]["generated_text"]


MAP_TYPE_TO_HANDLER = {
    type(ContentHandler): ContentHandler
}


class SagemakerEndpointWrapper(ModelWrapper):
    """Wrapper around custom Sagemaker Inference Endpoints.
    To use, you must supply the endpoint name from your deployed
    Sagemaker model & the region where it is deployed.
    To authenticate, the AWS client uses the following methods to
    automatically load credentials:
    https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html
    If a specific credential profile should be used, you must pass
    the name of the profile from the ~/.aws/credentials file that is to be used.
    Make sure the credentials / roles used have the required policies to
    access the Sagemaker endpoint.
    See: https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html
    """

    """
    Example:
            endpoint_name = ("my-endpoint-name")
            region_name = ("us-west-2")
            credentials_profile_name = ("default")
            se = SagemakerEndpointWrapper(
                endpoint_name=endpoint_name,
                region_name=region_name,
                credentials_profile_name=credentials_profile_name
            )
    """

    def __init__(self, 
                 name: str,
                 region: str, 
                 endpoint_name: str, 
                 content_handler: ContentHandlerBase,
                 model_kwargs: Optional[Dict] = None,
                 endpoint_kwargs: Optional[Dict] = None,
                 credentials_profile_name: Optional[str] = None) -> None:
        super().__init__()
        self.name = name
        self.region = region
        self.endpoint_name = endpoint_name
        self.content_handler = content_handler
        self.credentials_profile_name = credentials_profile_name
        self.endpoint_kwargs = endpoint_kwargs or {}
        self.model_kwargs = model_kwargs or {}
        self.client = None

        self.initialize()


    def initialize(self) -> None:
        """Validate that AWS credentials to and python package exists in environment."""

        try:
            if self.credentials_profile_name is not None:
                session = boto3.Session(profile_name=self.credentials_profile_name)
            else:
                session = boto3.Session()
            self.clinet = session.client(
                "sagemaker-runtime", region_name=self.region
            )

        except Exception as e:
            raise ValueError(
                "Could not load credentials to authenticate with AWS client. "
                "Please check that credentials in the specified "
                "profile name are valid."
            ) from e


    classmethod
    def get_description(cls) -> str:
        return """
            Sagemaker endpoint wrapper, allow accessing any model deployed in AWS Sagemaker using boto3
        """

    @classmethod
    def get_class_type_field(cls) -> str:
        return "sagemaker_endpoint"


    def to_json(self) -> Dict[str, Union[str, int]]:
        return {
            "region": self.region, 
            "endpoint_name": self.endpoint_kwargs, 
            "content_handler": type(self.content_handler),
            "model_kwargs": self.model_kwargs,
            "endpoint_kwargs": self.endpoint_kwargs,
            "credentials_profile_name": self.credentials_profile_name,
            "_class_type": self.get_class_type_field()
        }

    @classmethod
    def create_from_json(cls, json_key: str, json_data: Dict[str, str]) -> Any:
        content_handler = MAP_TYPE_TO_HANDLER(json_data["content_handler"])()
        return SagemakerEndpointWrapper(name=json_key, 
                                        region=json_data["region"], 
                                        endpoint_name=json_data["endpoint_name"],
                                        content_handler=content_handler,
                                        model_kwargs=json_data["model_kwargs"],
                                        endpoint_kwargs=json_data["endpoint_kwargs"],
                                        credentials_profile_name=json_data["credentials_profile_name"])


    def process(self, model_input: ModelIO) -> ModelIO:
        body = self.transform_input(model_input, self.model_kwargs)

        # send request
        try:
            response = self.client.invoke_endpoint(
                EndpointName=self.endpoint_name,
                Body=body,
                ContentType=self.content_handler.content_type,
                Accept=self.content_handler.accepts,
                **self.endpoint_kwargs,
            )
        except Exception as e:
            raise ValueError(f"Error raised by inference endpoint: {e}")

        text = self.content_handler.transform_output(response["Body"])

        return text

