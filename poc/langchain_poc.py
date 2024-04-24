import os
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate

# Instantiate Model
llm = AzureChatOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    openai_api_version="2023-03-15-preview",
    azure_deployment="infrawiz-gpt-4-vision-preview-integration",
    openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    openai_api_type="azure",
    temperature=0.7,
    max_tokens=1000
)

# Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an AI Chef. Create a unique recipe based on the following ingredient"),
        ("human", "{input}")
    ]
)

# Create LLM Chain
chain = prompt | llm

response = chain.invoke({"input": "tomatoes"})
print(response)
print(response.content)

# msg = HumanMessage(content="Which model are you?")
# output = llm(messages=[msg])
# print(output.content)
