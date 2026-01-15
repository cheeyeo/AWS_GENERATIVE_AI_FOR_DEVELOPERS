### AWS GENERATIVE AI FOR DEVELOPERS

Exercises from coursera course


#### Notes on Bedrock API

Amazon Bedrock provides several APIs for interacting with foundation models (FMs), enabling both synchronous and asynchronous inference. This guide explores the key APIs and their practical applications in building AI-powered solutions.

For examples of how to use Amazon Bedrock with boto3, visit the [Amazon Bedrock Samples repo]: https://github.com/aws-samples/amazon-bedrock-samples/tree/main



### Amazon Bedrock Endpoints

When you interact with AWS services through code, you connect to what’s called an endpoint. These are specific network addresses where your requests are sent. Amazon Bedrock uses several specialized endpoints to separate different types of functionality. When you’re writing code, you create different types of clients to connect to the various endpoints. Here's a breakdown of the main ones you will see throughout the videos:

* bedrock
This is the control plane for core model management. It includes APIs used to manage models. You’ll use this when you’re setting up resources or performing administrative actions.

bedrock-runtime
This is the data plane used for real-time inference. If you’re calling a model to generate output (e.g., text, images), your requests go through this endpoint. It's focused on running inference for the models you're using.

bedrock-agent
This is a control plane endpoint specifically for managing agents, prompt templates, knowledge bases, and prompt flows. You’ll use it when you're creating or configuring any of these components. You will learn more about these concepts in future lessons.

bedrock-agent-runtime
This is the data plane counterpart for agents. It’s used when you invoke an agent or flow, or when you query a knowledge base in real time. You will learn more about these concepts in future lessons.

### Amazon Bedrock APIs and their applications
InvokeModel API
Purpose: Synchronous model invocation for immediate responses

Key Features:

* Single request-response pattern

* Direct model interaction

* Suitable for real-time applications

Best for:

* Chatbots

* Interactive applications

* Real-time content generation

```
import boto3

client = boto3.client('bedrock-runtime')

response = client.invoke_model(    
     modelId='amazon.titan-text-express-v1',    
     body=json.dumps({        
          "inputText": "explain quantum computing",        
          "textGenerationConfig": {            
               "maxTokenCount": 500,            
               "temperature": 0.5,
               "topP": 0.9        
          }    
     })
)

print(json.loads(response['body'].read()))
```


InvokeModelWithResponseStream API
Purpose: Streaming responses for better user experience

Benefits:

* Real-time text generation

* Improved interactivity

* Ideal for chatbots and interactice applications

Best for:

* Interactive chat applications

* Real-time content generation

* User-facing applications 

* Live text generation displays


```
import boto3

import json

client = boto3.client('bedrock-runtime')

# Stream response example

response = client.invoke_model_with_response_stream(
     modelId='amazon.titan-text-express-v1',    
     body=json.dumps({        
          "inputText": "explain quantum computing",        
          "textGenerationConfig": {            
          "maxTokenCount": 500,            
          "temperature": 0.5,            
          "topP": 0.9
     }
  })
)

# Process the streaming response

for event in response.get('body'):    
     chunk = json.loads(event['chunk']['bytes'])
     print(chunk['outputText'], end='', flush=True)
```


StartAsyncInvoke API
Purpose: Asynchronous processing for time-consuming tasks

Key Features:

* Returns job ID immediately 

* Background processing

* Progress tracking capability

* No connection holding

Best for:

* Video generation

* Complex analysis tasks

* Long-run tasks

* Resource-intensive 

```
import boto3
import random

client = boto3.client('bedrock-runtime')

seed = random.randint(0, 2147483646)

prompt = "A robot painting a sunset"

model_input = {    
     "taskType": "TEXT_VIDEO",    
     "textToVideoParams": {"text": prompt},    
     "videoGenerationConfig": {        
          "fps": 24,        
          "durationSeconds": 6,        
          "dimension": "1280x720", 
          "seed": seed,    
     },
}

output_config = {    
     "s3OutputDataConfig": {        
          "s3Uri": "s3://<bucket_name>/<prefix>/"
     }
}

response = bedrock_runtime.start_async_invoke(    
     modelId="amazon.nova-reel-v1:0",
     modelInput=model_input,
     outputDataConfig=output_config,
)

print(response["invocationArn"])
```


CreateModelInvocationJob API
Purpose: Batch processing for large-scale operations

Key Features:

* S3 integration

* Parallel processing support

* Job orchestration handling

* Efficient resource utilization

Best for:

* Bulk content processing

* Customer support ticket analysis

* Large dataset processing

* Automated content classification

# Set up input and output S3 bucket configuration

```
inputDataConfig = {    
     "s3InputDataConfig": {        
          "s3Uri": "s3://<bucket_name>/<jsonl_file_name>"    
     }
}

outputDataConfig = {    
     "s3OutputDataConfig": {        
          "s3Uri": "s3://<bucket_name>/<prefix>/"    
     }
}

response = bedrock.create_model_invocation_job(
     roleArn=<role_arn>,
     modelId="anthropic.claude-3-haiku-20240307-v1:0",
     jobName="<job_name>",    
     inputDataConfig=inputDataConfig,
     outputDataConfig=outputDataConfig
)

job_arn = response.get("jobArn")
```


### Best Practices for API Usage

#### Error Handling
Error handling is crucial when working with Bedrock APIs. The example below demonstrates handling common exceptions like validation errors, timeouts, and unexpected issues. This pattern ensures your application gracefully handles failures and provides appropriate feedback:

```
def safe_model_invoke(prompt, model_id):    

try:        

    response = bedrock_runtime.invoke_model(            
          modelId=model_id,
          body=json.dumps({
               "inputText": prompt,
               "textGenerationConfig": {
                    "maxTokenCount": 512,
                    "temperature": 0.7
                } 
          })        

     )        
     return json.loads(response['body'].read())    
except bedrock_runtime.exceptions.ValidationException:        
     print("Invalid request parameters")
except bedrock_runtime.exceptions.ModelTimeoutException:        
     print("Model inference timed out")    
except Exception as e:        
     print(f"Unexpected error: {str(e)}")
```


### Request Rate Limiting

When making multiple API calls, it's important to implement rate limiting and exponential backoff to handle service quotas and prevent throttling.

### Response Handling

Different models return responses in varying formats. Always validate and properly parse the response body according to the model's specification.

### Other Key Considerations

#### Model Selection and Versioning

Each model has a unique modelId (e.g., 'anthropic.claude-v2', 'amazon.titan-text-express-v1')

Models are versioned, so be explicit about which version you're using

Different models have different capabilities, pricing, inference parameter support, and performance characteristics

#### Response Formats

Request and Response format vary by model and request type

Text models return JSON with generated content

Image models return base64-encoded image data

Streaming responses come in chunks that need to be assembled

#### API Limits and Quotas

Be aware of token limits per request

Consider concurrent request limits

Monitor API quotas and rate limits

Implement appropriate retry strategies




### On Prompt Management

Amazon Bedrock Prompt Management is a feature that enables developers to create, version, and reuse prompts across different workflows and applications. Instead of embedding prompts directly in application code, Prompt Management provides a centralized way to manage and optimize prompts for foundation models.


Prompt Management allows you to:
* Create and save prompts as reusable templates
* Version control your prompts
* Include variables (placeholders) in prompts
* Manage prompts across different environments (development, staging, production)

A prompt in Bedrock Prompt Management requires:
* Name
* One or more variants
* Template type (chat or text)
* Model configurations

e.g
```
prompt_name = "hr_assistant_prompt_template"
template_text = '''
You are an HR assistant.

Write a professional, inclusive job description using the following inputs:

Job title: {{job_title}}
Responsibilities: {{responsibilities}}
Requirements: {{requirements}}
Location: {{location}}
Work type: {{work_type}}

- Start with a clear summary
- Use concise, inclusive language
- Keep it under 250 words
'''

response = bedrock_agent.create_prompt(
    name=prompt_name,
    description="Generates inclusive job descriptions from structured inputs",
    defaultVariant="v1",
    variants=[
        {
            "name": "v1",
            "modelId": <MODEL_ID>,
            "templateType": "TEXT",
            "templateConfiguration": {
                "text": {
                    "inputVariables": [
                        {"name": "job_title"},
                        {"name": "responsibilities"},
                        {"name": "requirements"},
                        {"name": "location"},
                        {"name": "work_type"}
                    ],
                    "text": template_text
                }
            },
            "inferenceConfiguration": {
                "text": {
                    "maxTokens": 500,
                    "temperature": 0.7,
                    "topP": 0.9,
                    "stopSequences": []
                }
            }
        }
    ]
)
```

Each variant includes:
* Variant name
* Model ID
* Inference configuration ( temperature, topP, stopSequences )
* Template configuration

e.g.

```
variant_examples = [
    # First variant
    {
        "name": "detailed",
        "modelId": "<MODEL_ID>",
        "inferenceConfiguration": {
            "text" : {
              "temperature": 0.2,  # Lower temperature for more focused responses
              "topP": 0.9
            }
        }
    },
    # Second variant
    {
        "name": "summary",
        "modelId": "<MODEL_ID>",
        "inferenceConfiguration": {
            "text" : {
             "temperature": 0.7,  # Higher temperature for more focused responses
             "topP": 0.9
            }
        }
    }
]
```

Two main template types:
* Chat Template: for conversational format, includes system prompts and tool configurations
* Text Template: For single message prompts

You set the template type for the prompt by configuring the `templateType` parameter when you create the prompt. Valid values are TEXT or CHAT. 

CHAT is only compatible with models that support the 
Converse API. If you want to use prompt caching, you must use the CHAT template type.


Using Prompt Templates:
```
# With Converse API
response = bedrock.converse(    
     modelId="<prompt_arn>",    
     promptVariables={        
          'request': {            
               'text': "<request_content_here>"
        }
    },
)
```