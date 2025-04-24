import os
import logging
import json
from typing import Dict, List, Any, Optional, Union, BinaryIO
from datetime import datetime, timedelta

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

class AWSConnector:
    """
    Connector for interacting with AWS services using boto3.
    Provides methods for accessing S3, Lambda, Glue, and other AWS services.
    """
    
    def __init__(self, 
                 aws_access_key_id: str = None, 
                 aws_secret_access_key: str = None, 
                 aws_session_token: str = None,
                 region_name: str = None):
        """
        Initialize the AWS connector with credentials.
        If not provided, credentials will be loaded from environment variables
        or the AWS credentials file.
        """
        self.aws_access_key_id = aws_access_key_id or os.environ.get("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = aws_secret_access_key or os.environ.get("AWS_SECRET_ACCESS_KEY")
        self.aws_session_token = aws_session_token or os.environ.get("AWS_SESSION_TOKEN")
        self.region_name = region_name or os.environ.get("AWS_REGION", "us-east-1")
        
        # Initialize session and clients lazily
        self._session = None
        self._clients = {}
        self._resources = {}
    
    @property
    def session(self):
        """
        Get or create an AWS session.
        """
        if self._session is None:
            session_kwargs = {"region_name": self.region_name}
            
            # Add credentials if they were explicitly provided
            if self.aws_access_key_id and self.aws_secret_access_key:
                session_kwargs["aws_access_key_id"] = self.aws_access_key_id
                session_kwargs["aws_secret_access_key"] = self.aws_secret_access_key
                if self.aws_session_token:
                    session_kwargs["aws_session_token"] = self.aws_session_token
            
            self._session = boto3.Session(**session_kwargs)
            
        return self._session
    
    def get_client(self, service_name: str):
        """
        Get or create a boto3 client for a specific AWS service.
        """
        if service_name not in self._clients:
            self._clients[service_name] = self.session.client(service_name)
        return self._clients[service_name]
    
    def get_resource(self, service_name: str):
        """
        Get or create a boto3 resource for a specific AWS service.
        """
        if service_name not in self._resources:
            self._resources[service_name] = self.session.resource(service_name)
        return self._resources[service_name]
    
    # S3 Operations
    
    def list_buckets(self) -> List[Dict[str, Any]]:
        """
        List all S3 buckets.
        """
        try:
            response = self.get_client("s3").list_buckets()
            return [
                {
                    "name": bucket["Name"],
                    "creation_date": bucket["CreationDate"].isoformat()
                }
                for bucket in response.get("Buckets", [])
            ]
        except ClientError as e:
            logger.error(f"Error listing S3 buckets: {str(e)}")
            raise
    
    def list_objects(self, bucket_name: str, prefix: str = "", max_keys: int = 1000) -> List[Dict[str, Any]]:
        """
        List objects in an S3 bucket with optional prefix.
        """
        try:
            paginator = self.get_client("s3").get_paginator("list_objects_v2")
            page_iterator = paginator.paginate(
                Bucket=bucket_name,
                Prefix=prefix,
                PaginationConfig={"MaxItems": max_keys}
            )
            
            objects = []
            for page in page_iterator:
                for obj in page.get("Contents", []):
                    objects.append({
                        "key": obj["Key"],
                        "size": obj["Size"],
                        "last_modified": obj["LastModified"].isoformat(),
                        "etag": obj["ETag"],
                        "storage_class": obj["StorageClass"]
                    })
            
            return objects
        except ClientError as e:
            logger.error(f"Error listing objects in bucket {bucket_name}: {str(e)}")
            raise
    
    def upload_file(self, 
                    file_path: str, 
                    bucket_name: str, 
                    object_key: str = None, 
                    extra_args: Dict = None) -> bool:
        """
        Upload a file to S3.
        
        Args:
            file_path: Local path to the file
            bucket_name: S3 bucket name
            object_key: S3 object key (if None, uses the file name)
            extra_args: Additional arguments for S3 upload (e.g., ACL, ContentType)
        """
        if object_key is None:
            object_key = os.path.basename(file_path)
            
        try:
            self.get_client("s3").upload_file(
                Filename=file_path,
                Bucket=bucket_name,
                Key=object_key,
                ExtraArgs=extra_args
            )
            logger.info(f"Successfully uploaded {file_path} to s3://{bucket_name}/{object_key}")
            return True
        except ClientError as e:
            logger.error(f"Error uploading file {file_path} to S3: {str(e)}")
            raise
    
    def download_file(self, bucket_name: str, object_key: str, file_path: str) -> bool:
        """
        Download a file from S3.
        
        Args:
            bucket_name: S3 bucket name
            object_key: S3 object key
            file_path: Local path to save the file
        """
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            self.get_client("s3").download_file(
                Bucket=bucket_name,
                Key=object_key,
                Filename=file_path
            )
            logger.info(f"Successfully downloaded s3://{bucket_name}/{object_key} to {file_path}")
            return True
        except ClientError as e:
            logger.error(f"Error downloading file from S3: {str(e)}")
            raise
    
    def get_object(self, bucket_name: str, object_key: str) -> Dict[str, Any]:
        """
        Get an object from S3 and return its contents.
        """
        try:
            response = self.get_client("s3").get_object(
                Bucket=bucket_name,
                Key=object_key
            )
            
            body = response["Body"].read()
            try:
                # Try to parse as JSON
                content = json.loads(body)
            except json.JSONDecodeError:
                # If not JSON, return string content
                content = body.decode("utf-8")
                
            return {
                "content": content,
                "content_type": response.get("ContentType"),
                "content_length": response.get("ContentLength"),
                "last_modified": response.get("LastModified").isoformat() if response.get("LastModified") else None,
                "metadata": response.get("Metadata", {})
            }
        except ClientError as e:
            logger.error(f"Error getting object s3://{bucket_name}/{object_key}: {str(e)}")
            raise
    
    def put_object(self, 
                   bucket_name: str, 
                   object_key: str, 
                   content: Union[str, bytes, Dict, BinaryIO],
                   content_type: str = None) -> Dict[str, Any]:
        """
        Put an object to S3.
        
        Args:
            bucket_name: S3 bucket name
            object_key: S3 object key
            content: Content to upload (string, bytes, dictionary, or file-like object)
            content_type: Content type of the object
        """
        try:
            args = {}
            if content_type:
                args["ContentType"] = content_type
            
            # Convert content to appropriate format
            if isinstance(content, dict):
                content = json.dumps(content)
                if not content_type:
                    args["ContentType"] = "application/json"
            
            if isinstance(content, str):
                content = content.encode("utf-8")
                if not content_type:
                    args["ContentType"] = "text/plain"
            
            response = self.get_client("s3").put_object(
                Bucket=bucket_name,
                Key=object_key,
                Body=content,
                **args
            )
            
            logger.info(f"Successfully put object to s3://{bucket_name}/{object_key}")
            return {
                "etag": response.get("ETag"),
                "version_id": response.get("VersionId")
            }
        except ClientError as e:
            logger.error(f"Error putting object to s3://{bucket_name}/{object_key}: {str(e)}")
            raise
    
    def delete_object(self, bucket_name: str, object_key: str) -> bool:
        """
        Delete an object from S3.
        """
        try:
            self.get_client("s3").delete_object(
                Bucket=bucket_name,
                Key=object_key
            )
            logger.info(f"Successfully deleted object s3://{bucket_name}/{object_key}")
            return True
        except ClientError as e:
            logger.error(f"Error deleting object s3://{bucket_name}/{object_key}: {str(e)}")
            raise
    
    def generate_presigned_url(self, 
                              bucket_name: str, 
                              object_key: str, 
                              expiration: int = 3600, 
                              http_method: str = "GET") -> str:
        """
        Generate a presigned URL for an S3 object.
        
        Args:
            bucket_name: S3 bucket name
            object_key: S3 object key
            expiration: Time in seconds for the URL to remain valid
            http_method: HTTP method for the operation (GET, PUT, etc.)
        """
        try:
            url = self.get_client("s3").generate_presigned_url(
                ClientMethod=f"{http_method.lower()}_object",
                Params={"Bucket": bucket_name, "Key": object_key},
                ExpiresIn=expiration
            )
            logger.info(f"Generated presigned URL for s3://{bucket_name}/{object_key} valid for {expiration} seconds")
            return url
        except ClientError as e:
            logger.error(f"Error generating presigned URL: {str(e)}")
            raise
    
    def upload_file_to_s3(self, 
                    bucket: str, 
                    key: str, 
                    file_obj: BinaryIO, 
                    content_type: str = None) -> Dict[str, Any]:
        """
        Upload a file-like object to S3.
        
        Args:
            bucket: S3 bucket name
            key: S3 object key
            file_obj: File-like object with a read method
            content_type: Content type of the file
            
        Returns:
            Dictionary with information about the uploaded object
        """
        try:
            extra_args = {}
            if content_type:
                extra_args["ContentType"] = content_type
                
            # Upload using the file object directly
            s3_client = self.get_client("s3")
            s3_client.upload_fileobj(
                Fileobj=file_obj,
                Bucket=bucket,
                Key=key,
                ExtraArgs=extra_args
            )
            
            # Get information about the uploaded object
            response = s3_client.head_object(
                Bucket=bucket,
                Key=key
            )
            
            logger.info(f"Successfully uploaded object to s3://{bucket}/{key}")
            
            # Return information about the uploaded file
            return {
                "bucket": bucket,
                "key": key,
                "location": f"s3://{bucket}/{key}",
                "etag": response.get("ETag"),
                "version_id": response.get("VersionId"),
                "last_modified": response.get("LastModified").isoformat() if response.get("LastModified") else None,
                "content_length": response.get("ContentLength"),
                "content_type": response.get("ContentType")
            }
            
        except ClientError as e:
            logger.error(f"Error uploading file object to s3://{bucket}/{key}: {str(e)}")
            raise
    
    # Lambda Operations
    
    def list_lambda_functions(self, max_items: int = 50) -> List[Dict[str, Any]]:
        """
        List Lambda functions.
        """
        try:
            paginator = self.get_client("lambda").get_paginator("list_functions")
            page_iterator = paginator.paginate(
                PaginationConfig={"MaxItems": max_items}
            )
            
            functions = []
            for page in page_iterator:
                for function in page.get("Functions", []):
                    functions.append({
                        "name": function["FunctionName"],
                        "runtime": function.get("Runtime"),
                        "handler": function.get("Handler"),
                        "description": function.get("Description"),
                        "memory_size": function.get("MemorySize"),
                        "timeout": function.get("Timeout"),
                        "last_modified": function.get("LastModified"),
                        "role": function.get("Role"),
                        "code_size": function.get("CodeSize")
                    })
            
            return functions
        except ClientError as e:
            logger.error(f"Error listing Lambda functions: {str(e)}")
            raise
    
    def invoke_lambda(self, 
                    function_name: str, 
                    payload: Dict = None, 
                    invocation_type: str = "RequestResponse") -> Dict[str, Any]:
        """
        Invoke a Lambda function.
        
        Args:
            function_name: Name or ARN of the function
            payload: Input payload for the function (dictionary)
            invocation_type: RequestResponse, Event, or DryRun
        """
        try:
            invoke_args = {
                "FunctionName": function_name,
                "InvocationType": invocation_type
            }
            
            if payload:
                invoke_args["Payload"] = json.dumps(payload).encode()
            
            response = self.get_client("lambda").invoke(**invoke_args)
            
            result = {
                "status_code": response.get("StatusCode"),
                "executed_version": response.get("ExecutedVersion"),
                "log_result": response.get("LogResult")
            }
            
            if "Payload" in response:
                payload = response["Payload"].read()
                try:
                    result["payload"] = json.loads(payload)
                except json.JSONDecodeError:
                    result["payload"] = payload.decode("utf-8")
            
            logger.info(f"Successfully invoked Lambda function {function_name}")
            return result
        except ClientError as e:
            logger.error(f"Error invoking Lambda function {function_name}: {str(e)}")
            raise
    
    # Glue Operations
    
    def list_glue_jobs(self) -> List[Dict[str, Any]]:
        """
        List Glue jobs.
        """
        try:
            response = self.get_client("glue").get_jobs()
            return [
                {
                    "name": job["Name"],
                    "description": job.get("Description"),
                    "role": job.get("Role"),
                    "created": job.get("CreatedOn"),
                    "last_modified": job.get("LastModifiedOn"),
                    "worker_type": job.get("WorkerType"),
                    "num_workers": job.get("NumberOfWorkers"),
                    "max_capacity": job.get("MaxCapacity"),
                    "command": job.get("Command", {}).get("Name"),
                    "glue_version": job.get("GlueVersion")
                }
                for job in response.get("Jobs", [])
            ]
        except ClientError as e:
            logger.error(f"Error listing Glue jobs: {str(e)}")
            raise
    
    def start_glue_job_run(self, 
                         job_name: str, 
                         arguments: Dict[str, str] = None) -> Dict[str, Any]:
        """
        Start a Glue job run.
        
        Args:
            job_name: Name of the Glue job
            arguments: Job run arguments (dictionary of strings)
        """
        try:
            args = {"JobName": job_name}
            if arguments:
                args["Arguments"] = arguments
                
            response = self.get_client("glue").start_job_run(**args)
            logger.info(f"Successfully started Glue job {job_name}, run ID: {response.get('JobRunId')}")
            
            return {
                "job_name": job_name,
                "job_run_id": response.get("JobRunId")
            }
        except ClientError as e:
            logger.error(f"Error starting Glue job {job_name}: {str(e)}")
            raise
    
    def get_glue_job_run(self, job_name: str, run_id: str) -> Dict[str, Any]:
        """
        Get details of a Glue job run.
        
        Args:
            job_name: Name of the Glue job
            run_id: ID of the job run
        """
        try:
            response = self.get_client("glue").get_job_run(
                JobName=job_name,
                RunId=run_id
            )
            
            job_run = response.get("JobRun", {})
            return {
                "job_name": job_name,
                "job_run_id": run_id,
                "status": job_run.get("JobRunState"),
                "start_time": job_run.get("StartedOn").isoformat() if job_run.get("StartedOn") else None,
                "end_time": job_run.get("CompletedOn").isoformat() if job_run.get("CompletedOn") else None,
                "error_message": job_run.get("ErrorMessage"),
                "arguments": job_run.get("Arguments", {}),
                "allocated_capacity": job_run.get("AllocatedCapacity"),
                "execution_time": job_run.get("ExecutionTime"),
                "log_group_name": job_run.get("LogGroupName"),
                "max_capacity": job_run.get("MaxCapacity")
            }
        except ClientError as e:
            logger.error(f"Error getting Glue job run {job_name}/{run_id}: {str(e)}")
            raise
    
    # SageMaker Operations
    
    def list_sagemaker_notebooks(self) -> List[Dict[str, Any]]:
        """
        List SageMaker notebook instances.
        """
        try:
            response = self.get_client("sagemaker").list_notebook_instances()
            return [
                {
                    "name": instance["NotebookInstanceName"],
                    "status": instance["NotebookInstanceStatus"],
                    "instance_type": instance.get("InstanceType"),
                    "creation_time": instance.get("CreationTime").isoformat() if instance.get("CreationTime") else None,
                    "last_modified_time": instance.get("LastModifiedTime").isoformat() if instance.get("LastModifiedTime") else None,
                    "url": instance.get("Url")
                }
                for instance in response.get("NotebookInstances", [])
            ]
        except ClientError as e:
            logger.error(f"Error listing SageMaker notebook instances: {str(e)}")
            raise
    
    def list_sagemaker_endpoints(self) -> List[Dict[str, Any]]:
        """
        List SageMaker endpoints.
        """
        try:
            response = self.get_client("sagemaker").list_endpoints()
            return [
                {
                    "name": endpoint["EndpointName"],
                    "status": endpoint["EndpointStatus"],
                    "creation_time": endpoint.get("CreationTime").isoformat() if endpoint.get("CreationTime") else None,
                    "last_modified_time": endpoint.get("LastModifiedTime").isoformat() if endpoint.get("LastModifiedTime") else None
                }
                for endpoint in response.get("Endpoints", [])
            ]
        except ClientError as e:
            logger.error(f"Error listing SageMaker endpoints: {str(e)}")
            raise
    
    # CloudWatch Operations
    
    def get_logs(self, 
                log_group_name: str, 
                log_stream_name: str = None, 
                start_time: int = None, 
                end_time: int = None,
                limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get logs from CloudWatch Logs.
        
        Args:
            log_group_name: Name of the log group
            log_stream_name: Optional name of the log stream
            start_time: Start time in milliseconds since epoch
            end_time: End time in milliseconds since epoch
            limit: Maximum number of log events to return
        """
        try:
            params = {
                "logGroupName": log_group_name,
                "limit": limit
            }
            
            if log_stream_name:
                params["logStreamNames"] = [log_stream_name]
            if start_time:
                params["startTime"] = start_time
            if end_time:
                params["endTime"] = end_time
                
            response = self.get_client("logs").filter_log_events(**params)
            
            return [
                {
                    "timestamp": event["timestamp"],
                    "message": event["message"],
                    "log_stream_name": event.get("logStreamName")
                }
                for event in response.get("events", [])
            ]
        except ClientError as e:
            logger.error(f"Error getting logs from {log_group_name}: {str(e)}")
            raise
    
    # Validation
    
    def validate_connection(self) -> bool:
        """
        Test the connection to AWS.
        """
        try:
            # Try to list S3 buckets to validate connection
            self.list_buckets()
            logger.info("AWS connection validated")
            return True
        except Exception as e:
            logger.error(f"AWS connection validation failed: {str(e)}")
            return False
    
    def get_account_info(self) -> Dict[str, Any]:
        """
        Get information about the current AWS account.
        """
        try:
            sts_client = self.get_client("sts")
            response = sts_client.get_caller_identity()
            
            return {
                "account_id": response.get("Account"),
                "arn": response.get("Arn"),
                "user_id": response.get("UserId"),
                "region": self.region_name
            }
        except ClientError as e:
            logger.error(f"Error getting AWS account info: {str(e)}")
            raise


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Create connector using environment variables for credentials
    connector = AWSConnector()
    
    # Validate the connection
    is_valid = connector.validate_connection()
    print(f"Connection is valid: {is_valid}")
    
    if is_valid:
        # Get account info
        account_info = connector.get_account_info()
        print(f"Account ID: {account_info['account_id']}")
        print(f"Region: {account_info['region']}")
        
        # List S3 buckets
        buckets = connector.list_buckets()
        print(f"Found {len(buckets)} S3 buckets")
        for bucket in buckets[:5]:  # Print first 5 buckets
            print(f" - {bucket['name']} (created {bucket['creation_date']})")
        
        # List Lambda functions
        functions = connector.list_lambda_functions()
        print(f"Found {len(functions)} Lambda functions")
        for function in functions[:5]:  # Print first 5 functions
            print(f" - {function['name']} ({function['runtime']})") 