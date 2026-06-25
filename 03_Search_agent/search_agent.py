from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_openai import AzureChatOpenAI
from langchain.tools import tool
from tavily import TavilyClient

load_dotenv()

tavily = TavilyClient()

@tool
def search(query: str) -> str:
  """
  Tool that searches over internet
  Args:
    query: The query to search for
  Returns:
    The search result
  """
  print("Searching over the Internet")

  return tavily.search(query=query)


llm = AzureChatOpenAI(azure_deployment="gpt-4o")
tools = [search]
agent = create_agent(model = llm, tools = tools)

def main():
  print("Hello from langchian")
  result = agent.invoke({"messages":HumanMessage(content="What is Weather in Banglore")})
  print(result)

if __name__ == "__main__":
  main()