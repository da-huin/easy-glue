import re
import os
import time
import json
import boto3


class EasyGlue():
    """
    This package helps you use Glue easily. 

    **Parameters**

    * bucket_name

        S3 BUCKET NAME

    * jobs_base_dir

        A PLACE TO STORE JOBS SCRIPTS

    * aws_access_key_id

        AWS ACCESS KEY ID

    * aws_secret_access_key

        AWS SECRET ACCESS KEY

    * region_name

        AWS REGION

    """

    def __init__(self, bucket_name, jobs_base_dir: str="", aws_access_key_id: str = None, aws_secret_access_key: str = None, region_name: str = None):
        self._bucket_name = bucket_name
        self._jobs_base_dir = jobs_base_dir
        self._glue_client = boto3.client("glue",
                                         aws_access_key_id=aws_access_key_id,
                                         aws_secret_access_key=aws_secret_access_key,
                                         region_name=region_name)

        self._s3_client = boto3.client("s3",
                                       aws_access_key_id=aws_access_key_id,
                                       aws_secret_access_key=aws_secret_access_key,
                                       region_name=region_name)

        self._iam_client = boto3.client("iam",
                                       aws_access_key_id=aws_access_key_id,
                                       aws_secret_access_key=aws_secret_access_key,
                                       region_name=region_name)

    def deploy(self, job_name: str, max_capacity: int = 3, timeout: int = 7200, default_arguments: dict={}):
        """
        Use this function to deploy job into glue.

        **Parameters**

        * `(required) job_name`: str

            Name of glue job to be deployed.

        * `max_capacity`: int (default = 3)

            Max Capactiy of Glue Workers

        * `timeout`: int (default = 7200)

            Timeout of glue job

        * `default_arguments`: dict (default = {})

            Default Arguments of glue job. Detail refer to below.

            https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html        
        """
        role_name = "easy_glue_role"
        self._create_glue_role(role_name)
        job_dir = self._get_unique_service_path(self._jobs_base_dir, job_name)

        dest_path = f"easy_glue/jobs/{job_name}/index.py"
        index_path = f"{job_dir}/index.py"

        self._s3_client.upload_file(
            index_path, self._bucket_name, dest_path)


        base_default_arguments = {
            '--bucket_name': self._bucket_name,
            '--job-bookmark-option': 'job-bookmark-enable',
            "--enable-continuous-cloudwatch-log": "true",
            "--enable-continuous-log-filter": "true",
            "--TempDir": f"s3://{self._bucket_name}/easy_glue/temp"
        }


        base_default_arguments.update(default_arguments)


        job_args = {
            "Name": job_name,
            "Role": role_name,
            "DefaultArguments": base_default_arguments,
            "GlueVersion": '1.0',
            "MaxRetries": 0,
            "MaxCapacity": max_capacity,
            "Timeout": timeout,
            "Command": {
                'Name': 'glueetl', 'ScriptLocation': f's3://{self._bucket_name}/{dest_path}', 'PythonVersion': '3'}
        }
        try:
            self._glue_client.delete_job(JobName=job_name)
        except:
            pass

        return self._glue_client.create_job(**job_args)

    def run_crawler(self, crawler_name: str):
        """
        Use this function to Run Crawler

        **Parameters**

        * `(required) crawler_name`: str

        **Returns**

        * `Start crawler result`: dict
        """

        return self._glue_client.start_crawler(Name=crawler_name)

    def _create_glue_role(self, glue_role_name: str):
        
        try:
            self._iam_client.get_role(RoleName=glue_role_name)
        except:

            self._iam_client.create_role(RoleName=glue_role_name, AssumeRolePolicyDocument=json.dumps(
                {'Version': '2012-10-17', 'Statement': [{'Effect': 'Allow', 'Principal': {'Service': 'glue.amazonaws.com'}, 'Action': 'sts:AssumeRole'}]}))

            self._iam_client.attach_role_policy(
                RoleName=glue_role_name,
                PolicyArn="arn:aws:iam::aws:policy/AWSGlueConsoleFullAccess"
            )

        return glue_role_name

    def _get_unique_service_path(self, service_base_path: str, service_name: str):
        service_path = ""
        for dirpath, dirnames, _ in os.walk(service_base_path):
            if service_name in dirnames:
                service_path = os.path.abspath(dirpath + "/" + service_name)
                break

        if service_path == "":
            raise ValueError(
                f"{service_name} could not found in {service_base_path}")

        result = service_path.replace("\\", "/")
        if len(result.split("/")) == 1:
            raise ValueError(f"invalid service {service_name}")

        return result
