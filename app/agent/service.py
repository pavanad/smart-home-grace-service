import logging

from langchain import hub
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI

from app.settings import MODEL_NAME

from .tools.about import who_are_you
from .tools.cctv import cctv_image_analysis, cctv_list_cameras, cctv_send_images
from .tools.home import (
    smart_home_gate_state,
    smart_home_light_set_state,
    smart_home_lights_state,
)


class GraceService:
    def __init__(self):
        self.__logger = logging.getLogger(__name__)
        self._agent_executor = self.__create_grace_service()

    def __create_grace_service(self):
        self.__logger.info("Creating Grace Service")
        llm = ChatGoogleGenerativeAI(
            model=MODEL_NAME, convert_system_message_to_human=True
        )
        tools = [
            cctv_image_analysis,
            smart_home_lights_state,
            smart_home_gate_state,
            smart_home_light_set_state,
            who_are_you,
            cctv_send_images,
            cctv_list_cameras,
        ]
        prompt = hub.pull("hwchase17/structured-chat-agent")
        memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )
        agent = create_structured_chat_agent(llm, tools, prompt)
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
            handle_parsing_errors=True,
            memory=memory,
        )
        return agent_executor

    def execute(self, message: str) -> str:
        self.__logger.info(f"Executing Grace Service: {message}")
        message = f"{message}\nIMPORTANT: Always respond in Portuguese Brazil."
        result = self._agent_executor.invoke({"input": message})
        return result.get("output", "")
