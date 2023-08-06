from dataclasses import replace
from functools import partial
from typing import *

import telegram
import telegram.ext
from functional.option import *
from typing.io import *

from botter.api import BotBase
from botter.api.bot_api import *
from botter.util.os_operations import safe_remove

class TelegramUser(User):
    telegram_user: Optional[telegram.User]
    client: telegram.Bot
    
    # noinspection PyDataclass
    def __init__(self, client: telegram.Bot, user: telegram.User):
        self.telegram_user = user
        self.client = client
        
        super().__init__ \
        (
            id = self.telegram_user.id,
            user_name = self.telegram_user.name,
            display_name = self.telegram_user.full_name,
        )
    
    @property
    def mention(self) -> str:
        return self.telegram_user.mention_markdown()

class NoUser(TelegramUser):
    telegram_user: None
    # noinspection PyDataclass
    def __init__(self, client: telegram.Bot):
        self.telegram_user = None
        self.client = client
        
        super(TelegramUser, self).__init__ \
        (
            id = '#nouser#',
            user_name = 'NoUser',
            display_name = 'Not a User',
        )
    
    @property
    def mention(self) -> str:
        return '@NoUser'

TelegramValidAttachmentType = Union \
[
    telegram.PhotoSize,
    telegram.Sticker,
    telegram.Audio,
    telegram.Voice,
    telegram.Video,
    telegram.Document,
]
class TelegramAttachment(Attachment):
    telegram_attachment: TelegramValidAttachmentType
    client: telegram.Bot
    _f: Option[telegram.File] = Option.empty
    
    _at_type_map: Dict[Type[telegram.TelegramObject], AttachmentType] = \
    {
        telegram.PhotoSize:  AttachmentType.Image,
        telegram.Sticker:    AttachmentType.Image,
        telegram.Audio:      AttachmentType.Audio,
        telegram.Voice:      AttachmentType.Audio,
        telegram.Video:      AttachmentType.Video,
        telegram.Document:   AttachmentType.Document,
    }
    
    def __init__(self, client: telegram.Bot, attachment: TelegramValidAttachmentType):
        self.telegram_attachment = attachment
        self.client = client
        
        try:
            _type = Option(self._at_type_map.get(type(self.telegram_attachment), None)).get
        except EmptyOption:
            raise TypeError(f"'{self.telegram_attachment}' is not valid attachment")
        
        super().__init__ \
        (
            id = self.telegram_attachment.file_id,
            filename = self.telegram_attachment.file_name if (isinstance(self.telegram_attachment, telegram.Document)) else self.telegram_attachment.file_id,
            type = _type,
        )
    
    @property
    def file(self) -> telegram.File:
        self._f = self._f or Some(self.telegram_attachment.get_file())
        return self._f.get
    
    @property
    def weight(self) -> int:
        return Option(self.telegram_attachment.file_size).get_or_else(0)
    
    @property
    async def content(self) -> bytes:
        return bytes(self.file.download_as_bytearray())

class TelegramChannel(Channel):
    telegram_channel: telegram.Chat
    client: telegram.Bot
    
    # noinspection PyDataclass
    def __init__(self, client: telegram.Bot, channel: telegram.Chat):
        self.telegram_channel = channel
        self.client = client
        
        super().__init__ \
        (
            id = str(self.telegram_channel.id),
            name = (Option(self.telegram_channel.title) or Option(self.telegram_channel.first_name).flat_map(lambda first_name: Option(self.telegram_channel.last_name).map(lambda last_name: f'{first_name} {last_name}'))).get_or_else('Anonymous Chat'),
        )
    
    @classmethod
    async def from_id(cls, bot: Union[BotBase, telegram.Bot], channel_id: str) -> 'Channel':
        from .telegram_bot import TelegramBot
        
        client: telegram.Bot
        if (isinstance(bot, TelegramBot)):
            client = bot.client
        elif (isinstance(bot, telegram.Bot)):
            client = bot
        else:
            raise TypeError(f"Unsupported bot type, expected {TelegramBot} or {telegram.Bot}")
        
        return TelegramChannel(client, client.get_chat(int(channel_id)))
    
    async def fetch_message(self, id: str) -> 'InboundMessage':
        raise NotImplementedError
    
    async def send_message(self, message: 'Message'):
        return await send_message(self.telegram_channel, message)
    
    async def send_typing(self, enabled: bool = True):
        raise NotImplementedError

class TelegramMessage(InboundMessage):
    telegram_message: telegram.Message
    client: telegram.Bot
    author: TelegramUser
    
    # noinspection PyDataclass
    def __init__(self, client: telegram.Bot, message: telegram.Message):
        self.telegram_message = message
        self.client = client
        
        attachments: List[Optional[TelegramValidAttachmentType]] = \
            self.telegram_message.photo + \
            [
                self.telegram_message.sticker,
                self.telegram_message.audio,
                self.telegram_message.voice,
                self.telegram_message.video,
                self.telegram_message.document,
            ]
        attachments: Iterable[TelegramValidAttachmentType] = filter(None, attachments)
        
        author = Option(self.telegram_message.from_user) \
            .map(lambda u: TelegramUser(client, u)) \
            .get_or_else(NoUser(client)) \
        
        super().__init__ \
        (
            id = self.telegram_message.message_id,
            text = (Option(self.telegram_message.text) or Option(self.telegram_message.caption) or Some('')).get,
            attachments = [ TelegramAttachment(client, att) for att in attachments ],
            author = author,
            channel = TelegramChannel(client, self.telegram_message.chat),
            mentions = [ TelegramUser(client, u.user) for u in message.entities if u.user is not None ]
        )
    
    async def reply(self, message: Message):
        await send_message(self.telegram_message.chat, replace(message, text=f"{self.author.mention},\n{message.text}"))
    
    async def edit(self, new_text: str):
        self.client.edit_message_text(text=new_text, chat_id=self.channel.id, message_id=self.id)
    
    async def delete(self):
        self.client.delete_message(chat_id=self.channel.id, message_id=self.id)

async def send_message(channel: telegram.Chat, message: Message):
    text = message.text.strip()
    channel.send_message(text or None, parse_mode=telegram.ParseMode.MARKDOWN)
    for at in message.attachments:
        tmp_file = await at.temp_file
        with open(tmp_file, 'rb') as f:
            get_upload_file_func(channel, at)(f)
        safe_remove(tmp_file)

# noinspection PyTypeChecker
def get_upload_file_func(channel: telegram.Chat, attachment: Attachment) -> Callable[[BinaryIO], None]:
    if (attachment.type == AttachmentType.Image):
        return partial(channel.send_photo)
    elif (attachment.type == AttachmentType.Audio):
        return partial(channel.send_audio)
    elif (attachment.type == AttachmentType.Video):
        return partial(channel.send_video)
    else:
        return partial(channel.send_document, filename=attachment.filename)

__all__ = \
[
    'TelegramAttachment',
    'TelegramChannel',
    'TelegramMessage',
    'TelegramUser',
    
    'send_message',
]
