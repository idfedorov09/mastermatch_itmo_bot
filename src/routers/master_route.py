from aiogram import Router, Bot
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from langchain.agents import create_react_agent, AgentExecutor
from langchain_openai import ChatOpenAI

from ..states.states import RunState
from ..models.models import User
from ..common.context_manager import ContextManager

master_router = Router()
sources = ['https://abit.itmo.ru/program/master/ai', 'https://abit.itmo.ru/program/master/ai_product']

@master_router.message(
    CommandStart()
)
async def start_command_handler(
        message: Message,
        bot: Bot,
        state: FSMContext,
):
    user = await ContextManager.get(User)
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"Привет! Я - ассистент по подбору подходящей программы в ИТМО. Опиши свои компетенции",
    )
    await state.set_state(RunState.enter_comp)


@master_router.message(
    RunState.enter_comp
)
async def handle_enter_comp(
        message: Message,
        bot: Bot,
        state: FSMContext,
):
    llm = ChatOpenAI(
        model='gpt-4.1',
        max_retries=3
    )
    text = message.text.strip()
    text = (f"Привет! Я будущий студент ИТМО, вот мои компетенции: {text}."
            f"Помоги выбрать программу. Вот список возможных:")

    # TODO: стейт после этого
    # TODO: тулза для просмотра интернет-страниц и файлов с ней

    agent = AgentExecutor(
        agent=llm,
        tools=[],# TODO
        max_iterations=4,
    )

    resp = agent.invoke({'content': 'TODO: PROMPT', 'parallel_tool_calls': True}).get('output')
    await message.reply(resp)
