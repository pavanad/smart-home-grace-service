from langchain import hub
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from app.settings import MODEL_NAME

from .tools import cctv_image_analysis, smart_home_control, who_are_you


class GraceService:
    def __init__(self):
        self._agent_executor = self.__create_grace_service()

    def __create_grace_service(self):
        tools = [cctv_image_analysis, smart_home_control, who_are_you]
        llm = ChatGoogleGenerativeAI(
            model=MODEL_NAME, convert_system_message_to_human=True
        )
        prompt = hub.pull("hwchase17/structured-chat-agent")
        agent = create_structured_chat_agent(llm, tools, prompt)
        agent_executor = AgentExecutor(
            agent=agent, tools=tools, verbose=True, handle_parsing_errors=True
        )
        return agent_executor

    def execute(self, query: str) -> str:
        result = self._agent_executor.invoke({"input": query})
        return result.get("output", "")
