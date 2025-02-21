import dataclasses
import typing

import aiogram
import aiogram.filters
import aiogram.types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, on
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dishka.integrations.aiogram import FromDishka, inject

from app.core.domain.campaign.service.dto import Gender, TargetingDTO
from app.core.domain.campaign.service.usecases import CampaignUsecase
from app.core.infra.models.telegram_advertisers.interface import (
    TelegramAdvertisersRepository,
)

menu_router = aiogram.Router()


@menu_router.message(aiogram.filters.Command('menu'))
@inject
async def menu(
    message: aiogram.types.Message,
    state: FSMContext,
    repository: FromDishka[TelegramAdvertisersRepository],
    usecase: FromDishka[CampaignUsecase],
) -> None:
    advertiser_id = await repository.get_advertiser(str(message.from_user.id))
    campaigns = await usecase.get_advertiser_campaigns(advertiser_id)

    keyboard = InlineKeyboardBuilder()

    for campaign in campaigns:
        keyboard.button(
            text=campaign.ad_title,
            callback_data=f'campaign:{campaign.id}',
        )

    keyboard.button(
        text='Создать кампанию',
        callback_data='create_campaign',
    )

    keyboard.adjust(1)

    await message.answer('Ваши кампании:', reply_markup=keyboard.as_markup())


@dataclasses.dataclass
class Field:
    name: str
    text: str


questions = [
    Field(
        name='impressions_limit',
        text='Введите максимальное количество показов',
    ),
    Field(
        name='clicks_limit',
        text='Введите максимальное количество переходов',
    ),
    Field(
        name='cost_per_click',
        text='Введите стоимость за клик',
    ),
    Field(
        name='cost_per_impression',
        text='Введите стоимость за показ',
    ),
    Field(
        name='ad_title',
        text='Введите заголовок объявления',
    ),
    Field(
        name='ad_text',
        text='Введите текст объявления',
    ),
    Field(
        name='start_date',
        text='Введите дату начала кампании (число)',
    ),
    Field(
        name='end_date',
        text='Введите дату завершения кампании (число)',
    ),
    Field(
        name='gender',
        text='Выберите целевую аудиторию по полу (MALE / FEMALE / ALL)',
    ),
    Field(
        name='age_from',
        text='Введите минимальный возраст целевой аудитории',
    ),
    Field(
        name='age_to',
        text='Введите максимальный возраст целевой аудитории',
    ),
    Field(
        name='location',
        text='Введите местоположение целевой аудитории',
    ),
]


class CampaignCreationScene(Scene, state='campaign_creation'):
    @on.message.enter()
    async def on_enter(self, message: aiogram.types.Message, state: FSMContext):
        data = await state.get_data()
        data['step'] = 0
        data['answers'] = {}
        await state.set_data(data)

        question = questions[data['step']]

        await message.answer(
            'Пожалуйста, заполните следующие поля кампании. '
            'Валидация произойдет в конце.'
        )
        return await message.answer(question.text)

    @on.message(aiogram.F.text)
    async def on_answer(
        self,
        message: aiogram.types.Message,
        state: FSMContext,
    ) -> typing.Any:
        data = await state.get_data()
        step = data['step']

        question = questions[step]

        data['answers'][question.name] = message.text
        data[step] = step + 1 if step + 1 < len(questions) else None
        await state.set_data(data)

        if data[step] is not None:
            new_question = questions[data[step]]
            return await message.answer(new_question.text)

        await self.wizard.exit(success=True)

    @on.message.exit()
    @inject
    async def on_exit(
        self,
        message: aiogram.types.Message,
        state: FSMContext,
        repository: FromDishka[TelegramAdvertisersRepository],
        usecase: FromDishka[CampaignUsecase],
        success: bool,
    ) -> typing.Any:
        if not success:
            return None

        data = await state.get_data()
        answers = data['answers']

        targeting_dto = TargetingDTO(
            gender=Gender(answers['gender']),
            age_from=int(answers['age_from']),
            age_to=int(answers['age_to']),
            lo
        )

        return await message.answer(
            f'Вы успешно зарегистрировали кампанию "{dto.name}". ID: {dto.id}'
        )
