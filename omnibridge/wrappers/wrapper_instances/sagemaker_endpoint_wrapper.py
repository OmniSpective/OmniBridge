"""Wrapper around Sagemaker InvokeEndpoint API."""
from typing import Any, Dict, Optional, Tuple

from ..wrapper_interfaces.model_wrapper import ModelWrapper
from .preprocessors import PreprocessorBase, MAP_PREPROCESS_TYPE_TO_HANDLER
from .postprocessors import PostprocessorBase, MAP_POSTPROCESS_TYPE_TO_HANDLER
from omnibridge.model_entities.models_io.base_model_io import ModelIO
import boto3 # type: ignore




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
                 content_handlers: Tuple[PreprocessorBase, PostprocessorBase],
                 model_kwargs: Optional[Dict] = None,
                 endpoint_kwargs: Optional[Dict] = None,
                 credentials_profile_name: Optional[str] = None) -> None: 
        super().__init__()

        # enfore content_handlers
        if len(content_handlers) != 2:
            raise Exception(f"content_handlers has len {len(content_handlers)}, must have exactly 2 items")
        if not (isinstance(content_handlers[0], PreprocessorBase) and \
                isinstance(content_handlers[1], PostprocessorBase)):
            raise Exception("""
                content_handlers[0] must inherit from PreprocessorBase, 
                content_handlers[1] must inherit from PostprocessorBase.
            """)

        self.name: str = name
        self.region: str = region
        self.endpoint_name: str = endpoint_name
        self.content_handlers: Tuple[PreprocessorBase, PostprocessorBase] = content_handlers
        self.credentials_profile_name: Optional[str] = credentials_profile_name
        self.endpoint_kwargs: Dict = endpoint_kwargs or {}
        self.model_kwargs: Dict = model_kwargs or {}

        self.initialize()

    def get_name(self) -> str:
        return self.name

    def initialize(self) -> None:
        """Validate that AWS credentials to and python package exists in environment."""

        try:
            if self.credentials_profile_name is not None:
                session = boto3.Session(profile_name=self.credentials_profile_name)
            else:
                session = boto3.Session()
            self.client = session.client(
                "sagemaker-runtime", region_name=self.region
            )

        except Exception as e:
            raise ValueError(
                "Could not load credentials to authenticate with AWS client. "
                "Please check that credentials in the specified "
                "profile name are valid."
            ) from e

    @classmethod
    def get_description(cls) -> str:
        return """
            Sagemaker endpoint wrapper, allow accessing any model deployed in AWS Sagemaker using boto3
        """

    @classmethod
    def get_class_type_field(cls) -> str:
        return "sagemaker_endpoint"


    def to_json(self) -> Dict[str, Any]:
        return {
            "region": self.region, 
            "endpoint_name": self.endpoint_kwargs, 
            "content_handlers": {
                "preprocess": self.content_handlers[0].get_name(),
                "postprocess": self.content_handlers[1].get_name()
            },
            "model_kwargs": self.model_kwargs,
            "endpoint_kwargs": self.endpoint_kwargs,
            "credentials_profile_name": self.credentials_profile_name,
            "_class_type": self.get_class_type_field()
        }

    @classmethod
    def create_from_json(cls, json_key: str, json_data: Dict[str, Any]) -> Any:
        preprocessor = MAP_PREPROCESS_TYPE_TO_HANDLER[json_data["content_handlers"]["preprocess"]]()
        postprocessor = MAP_POSTPROCESS_TYPE_TO_HANDLER[json_data["content_handlers"]["postprocess"]]()

        return SagemakerEndpointWrapper(name=json_key, 
                                        region=json_data["region"], 
                                        endpoint_name=json_data["endpoint_name"],
                                        content_handlers=(preprocessor, postprocessor),
                                        model_kwargs=json_data["model_kwargs"],
                                        endpoint_kwargs=json_data["endpoint_kwargs"],
                                        credentials_profile_name=json_data["credentials_profile_name"])


    def process(self, model_input: ModelIO) -> ModelIO:
        body = self.content_handlers[0].transform_input(prompt=model_input, model_kwargs=self.model_kwargs)

        # send request
        try:
            response = self.client.invoke_endpoint(
                EndpointName=self.endpoint_name,
                Body=body,
                ContentType=self.content_handlers[0].content_type,
                Accept=self.content_handlers[1].accepts,
                **self.endpoint_kwargs,
            )
        except Exception as e:
            raise ValueError(f"Error raised by inference endpoint: {e}")

        result = self.content_handlers[1].transform_output(output=response["Body"])

        return result

