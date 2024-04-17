from configurations.db import *
from configurations.openai import *


def prompt_generate_diagram_analysis(image_url: str):
    prompt = (
        "Identify each component and their relevant upstream & downstream components with the sequence"
    )

    # "In the diagram, identify each component and their relevant upstream & downstream components along with the sequence"

    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": "You are an AI assistant that helps people find information."},
            {"role": "user", "content": [
                {
                    "type": "text",
                    "text": prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_url
                    }
                }
            ]}
        ],
        max_tokens=4000
    )
    response_message = response.choices[0].message.content

    print("*************************** GENERATED ANALYSIS ***********************")
    print(response_message)
    print("**********************************************************************")

    return response_message


def prompt_generate_json(project_name: str):
    existing_project = collection_projects.find_one({"project_name": project_name})

    # ==================================================================================================================
    prompt = (
        "I want you to build a JSON file using the Architecture Diagram Analysis which I will provide.\n"
        "It has each components listed along with their upstream & downstream components as well.\n"
        "I want you to take those upstream/downstream components into consideration when generating the JSON file.\n"
        "Here's the analysis:\n"
    )

    analysis = ''
    if existing_project:
        analysis = existing_project.get('diagram_analysis')

    prompt_followup = ("I want something in the following format:\n"
                       "Ex:\n")

    sample_json_content = """
        {
          "cloud_environment": "AWS",
          "components": [
            {
              "type": "ServerlessFunction",
              "name": "LambdaFunction1",
              "description": "Handles image processing and uploads to S3",
              "runtime": "Node.js",
              "dependencies": ["S3Bucket1", "DynamoDBTable1"],
              "configurations": {
                "timeout": 30,
                "memory_size": 256,
                "environment_variables": {
                  "AWS_REGION": "us-east-1",
                  "LOG_LEVEL": "DEBUG"
                }
              }
            },
            {
              "type": "Microservice",
              "name": "UserService",
              "description": "Manages user data",
              "dependencies": ["DynamoDBTable1"],
              "configurations": {
                "replica_count": 3,
                "cpu": "0.5",
                "memory": "512Mi"
              }
            },
            {
              "type": "WorkerService",
              "name": "BackgroundWorker",
              "description": "Processes background tasks",
              "dependencies": ["S3Bucket1"],
              "configurations": {
                "replica_count": 2,
                "cpu": "0.3",
                "memory": "256Mi"
              }
            }
            // ... other components
          ],
          "clusters": [
            {
              "type": "KubernetesCluster",
              "name": "EKSCluster1",
              "description": "Orchestrates microservices and worker services",
              "components": [
                {
                  "type": "ServerlessFunction",
                  "name": "LambdaFunction1"
                },
                {
                  "type": "Microservice",
                  "name": "UserService"
                },
                {
                  "type": "WorkerService",
                  "name": "BackgroundWorker"
                }
                // ... other services
              ]
            }
          ]
        }
        """

    prompt_closure = ("\nI don't want any other text output apart from the JSON file, because I intend to reuse it")
    # ==================================================================================================================

    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": "You are an AI assistant that helps people find information."},
            {"role": "user", "content": [
                {
                    "type": "text",
                    "text": prompt
                },
                {
                    "type": "text",
                    "text": analysis
                },
                {
                    "type": "text",
                    "text": prompt_followup
                },
                {
                    "type": "text",
                    "text": sample_json_content
                },
                {
                    "type": "text",
                    "text": prompt_closure
                }
            ]}
        ],
        max_tokens=4000
    )

    response_message = response.choices[0].message.content
    print("*************************** GENERATED JSON ***************************")
    print(response_message)
    print("**********************************************************************")

    return response_message


def prompt_generate_iac(project_name: str):
    existing_project = collection_projects.find_one({"project_name": project_name})

    # ==================================================================================================================
    prompt = (
        "I want you to build a Terraform script using the JSON file which I will provide.\n"
        "Here's the JSON file content:\n"
    )

    json_content = ''
    if existing_project:
        json_content = existing_project.get('json_data')

    prompt_followup = ("I want something in the following format:\n"
                       "Ex:\n")

    sample_iac_content = """
            provider "aws" {
              region = "us-east-1"
            }

            # Serverless Function: LambdaFunction1
            resource "aws_lambda_function" "lambda_function_1" {
              function_name = "LambdaFunction1"
              description   = "Handles image processing and uploads to S3"
              runtime       = "nodejs14.x"
              timeout       = 30
              memory_size   = 256

              environment = {
                AWS_REGION = "us-east-1"
                LOG_LEVEL  = "DEBUG"
              }

              # Add necessary IAM role configuration

              # Add dependencies
              depends_on = [
                aws_s3_bucket.s3_bucket_1,
                aws_dynamodb_table.dynamodb_table_1,
              ]
            }

            # Microservice: UserService
            resource "kubernetes_deployment" "user_service" {
              metadata {
                name = "UserService"
              }

              spec {
                replicas = 3

                template {
                  spec {
                    container {
                      name  = "user-service"
                      image = "your-docker-image"

                      # Add necessary configurations
                    }
                  }
                }
              }

              # Add dependencies
              depends_on = [
                aws_dynamodb_table.dynamodb_table_1,
              ]
            }

            # Worker Service: BackgroundWorker
            resource "kubernetes_deployment" "background_worker" {
              metadata {
                name = "BackgroundWorker"
              }

              spec {
                replicas = 2

                template {
                  spec {
                    container {
                      name  = "background-worker"
                      image = "your-docker-image"

                      # Add necessary configurations
                    }
                  }
                }
              }

              # Add dependencies
              depends_on = [
                aws_s3_bucket.s3_bucket_1,
              ]
            }

            # S3 Bucket: S3Bucket1
            resource "aws_s3_bucket" "s3_bucket_1" {
              bucket = "s3-bucket-1"
              acl    = "private"
              versioning {
                enabled = true
              }
            }

            # DynamoDB Table: DynamoDBTable1
            resource "aws_dynamodb_table" "dynamodb_table_1" {
              name           = "DynamoDBTable1"
              description    = "Stores metadata of processed images"
              read_capacity  = 5
              write_capacity = 5

              attribute {
                name = "ImageID"
                type = "S"
              }

              attribute {
                name = "Timestamp"
                type = "N"
              }

              key {
                attribute_name = "ImageID"
                attribute_type = "S"
              }

              # Add other necessary configurations
            }

            # Kubernetes Cluster: EKSCluster1
            module "eks_cluster_1" {
              source       = "terraform-aws-modules/eks/aws"
              cluster_name = "EKSCluster1"

              # Add necessary configurations and dependencies
            }

            # ... other resources and configurations for the cluster

            # ... other clusters and resources
            """

    prompt_closure = (
        "\nI don't want any other text output apart from the Terraform Script. So please avoid adding any other text")
    # ==================================================================================================================

    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": "You are an AI assistant that helps people find information."},
            {"role": "user", "content": [
                {
                    "type": "text",
                    "text": prompt
                },
                {
                    "type": "text",
                    "text": json_content
                },
                {
                    "type": "text",
                    "text": prompt_followup
                },
                {
                    "type": "text",
                    "text": sample_iac_content
                },
                {
                    "type": "text",
                    "text": prompt_closure
                }
            ]}
        ],
        max_tokens=4000
    )

    response_message = response.choices[0].message.content

    print("*************************** GENERATED IAC ****************************")
    print(response_message)
    print("**********************************************************************")

    return response_message