### Bedrock Agents

https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html

https://docs.aws.amazon.com/bedrock/latest/userguide/service_code_examples_bedrock-agent.html

https://docs.aws.amazon.com/bedrock/latest/APIReference/API_Operations_Agents_for_Amazon_Bedrock.html

https://strandsagents.com/0.1.x/


Bedrock Agents simplifies AI application development by managing complex interactions between foundation models, data sources and APIs.

Success depends on clear agent instructions, well-designed action groups, and effective use of memory and knowledge bases.

Start with a clear use case, implement proper versioning, and continuously refine agents based on user interactions.

#### Key components and capabilities

#### Foundation Model integration

When creating an agent:
* Select from AWS's collection of foundation models available through Amazon Bedrock

* Configure the model to align with your use case through system prompt configuration

* Let the agent use this model to process user inputs, determine when tools are needed, and orchestrate responses


#### Agent Instructions
Think of agent instructions as your agent's mission statement and operating manual combined. These instructions define the boundaries and personality of your agent, guiding its interactions and decision-making processes.

For example, an HR assistant agent might be instructed to:

* Verify employee eligibility
* Check available leave balance
* Process vacation requests
* Maintain a professional, helpful tone


#### Code Interpretation
Code interpretation allows agents to generate and execute code in a secure sandbox environment, enabling:

* Real-time data analysis
* Complex calculations
* Format conversions
* Data visualization
* Custom data processing workflows


#### Interactive User Inputs
The interactive nature of Bedrock Agents is demonstrated through its sophisticated conversation management. During interactions, agents can:

* Request specific information when needed
* Validate user inputs
* Maintain context throughout the interaction
* Guide users through multi-step processes


#### Action Groups
Agent's toolkit for executing tasks. These action groups can include Lambda functions, API Integrations, and custom tools.

Agents can also connect to knowledge bases to access resources like:
* Company policies
* Product documentation
* Technical guides
* FAQs
* Historical data


#### Memory

Maintain conversation context through memory capabilities.

Memory enables agents to:
* Retain context across multiple user sessions
* Recall and reference past interactions
* Store summarized conversations using the foundation model
* Configure retention periods by:
  * Number of days
  * Number of sessions
* Access relevant historical information when needed


#### Knowledge Base Integration

Can associate agent with 1 or more knowledge bases to enhance their responses: This include:
* Enables Retrieval Augmented Generation (RAG)
* Allows agents to access domain-specific information such as:
  * Corporate policies
  * Technical documentation
  * Product information
  * Training materials
  * Augments LLM responses with verified information

* Provides real-time access to updated company knowledge
* Helps ensure accurate and consistent responses


#### Orchestration
i.e. use orchestrator agent to break down tasks and delegate to other more specific agents


Use orchestration prompts to manage complex tasks and interactions. The orchestration process:

* Combines multiple components to build comprehensive responses:
  * Agent instructions
  * Action group definitions
  * Knowledge base content

* Uses system instructions alongside user chat interactions

* Comes with default prompt templates for common scenarios

* Allows customization through advanced prompts for specific needs

* Manages flow of:
  * User requests
  * Model interactions
  * Function calls
  * Data retrieval

#### Multi-agent collaboration

Bedrock Agents can work together as collaborators to handle complex workflows. This collaboration enables:

* Association of multiple specialized agents
* Reuse of existing agent capabilities, such as:
  * Flight booking agents
  * Calendar management agents
  * Data processing agents
* Orchestration of responses across multiple agents
* Division of complex tasks into specialized functions
* Seamless handoff between different agent capabilities
* Maintenance of context across agent interactions

#### Strands Agents SDK

Ref: https://strandsagents.com/0.1.x/

open source framework for agentic applications

Lightweight and gets out of your way: A simple agent loop that just works and is fully customizable.

Production ready: Full observability, tracing, and deployment options for running agents at scale.

Model, provider, and deployment agnostic: Strands supports many different models from many different providers.

Powerful built-in tools: Get started quickly with tools for a broad set of capabilities.

Multi-agent and autonomous agents: Apply advanced techniques to your AI systems like agent teams and agents that improve themselves over time.

Conversational, non-conversational, streaming, and non-streaming: Supports all types of agents for various workloads.

Safety and security as a priority: Run agents responsibly while protecting data.