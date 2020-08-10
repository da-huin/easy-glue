<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="./static/icon.png" alt="Project logo" ></a>
 <br>

 
</p>

<h3 align="center">Easy Glue</h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![GitHub Issues](https://img.shields.io/github/issues/da-huin/easy_glue.svg)](https://github.com/da-huin/easy_glue/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/da-huin/easy_glue.svg)](https://github.com/da-huin/easy_glue/pulls)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>

---

<p align="center"> This package helps you use AWS Glue easily. 
    <br> 
</p>

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Acknowledgments](#acknowledgement)

## 🧐 About <a name = "about"></a>

You can use following functions.

* [deploy](#deploy)
* [run_crawler](#run_crawler)

## 🏁 Getting Started <a name = "getting_started"></a>

### Installing

* If you want save as parquet format, install `pandas` and `fastparquet`.

```
pip install easy_glue
```

<a name="prerequisites"></a>

### Prerequisites 

#### 1. (Required) Create Handler

Use this code to create handler.

```python
import easy_glue

bucket_name = "YOUR BUCKET NAME"

# You don't need to use these parameters if your authentication file is in ~/.aws/config.
aws_access_key_id = "YOUR AWS ACCESS KEY ID"
aws_secret_access_key = "YOUR AWS SECRET ACCESS KEY"
region_name = "YOUR AWS REGION"

# You need to create this directory.
jobs_base_dir = "YOUR A PLACE TO STORE JOBS SCRIPTS"

handler = easy_glue.EasyGlue(bucket_name, jobs_base_dir=jobs_base_dir, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)

print(handler)
```

result:
```
<easy_glue.EasyGlue object at 0x016EE7F0>
```

## 🎈 Usage <a name="usage"></a>

Please check [Prerequisites](#prerequisites) before starting `Usage`.

### 🌱 deploy <a name="deploy"></a>

Use this function to deploy job into glue.

**Tutorial**

1. Create a directory `sample_job` in `YOUR_JOBS_BASE_DIR`.

1. Create a py file `index.py` in `YOUR_JOBS_BASE_DIR/sample_job`.

1. Write `Spark` code in `YOURJOBS_BASE_DIR/sample_job/index.py`.

1. Deploy `sample_job` as the code below.

    ```python
    >>> print(handler.deploy("sample_job"))
    ```

    Execution Result:
    ```python
    {'Name': 'sample_job', 'ResponseMetadata': {'RequestId': 'e436b350-7b36-47f4-b663-df52a058c2cb', 'HTTPStatusCode': 200, 'HTTPHeaders': {'date': 'Mon, 10 Aug 2020 03:53:56 GMT', 'content-type': 'application/x-amz-json-1.1', 'content-length': '21', 'connection': 'keep-alive', 'x-amzn-requestid': 'e436b350-7b36-47f4-b663-df52a058c2cb'}, 'RetryAttempts': 0}}
    ```

1. You can find deployed job in a glue console.

    https://ap-northeast-2.console.aws.amazon.com/glue/home?2#etl:tab=jobs


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

**Returns**

* `Create job result`: dict

### 🌱 run_crawler <a name="run_crawler"></a>

Use this function to Run Crawler

**Parameters**

* `(required) crawler_name`: str

**Returns**

* `Start crawler result`: dict

## 🎉 Acknowledgements <a name = "acknowledgement"></a>

- Title icon made by [Freepik](https://www.flaticon.com/kr/authors/freepik).

- If you have a problem. please make [issue](https://github.com/da-huin/easy_glue/issues).

- Please help develop this project 😀

- Thanks for reading 😄
