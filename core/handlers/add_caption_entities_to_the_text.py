from aiogram.types import Message


def modify_text(message: Message) -> str:
    """add caption entities if some_text string unfilled,
    else <Message.text> to the message text"""
    if message.text:
        new_message = message.text
        entities = message.entities
    else:
        if not message.caption:
            return ''
        new_message = message.caption
        entities = message.caption_entities

    if not entities:
        return new_message

    for entity in entities:
        tags = {'bold': 'b',
                'italic': 'i',
                'underline': 'u',
                'strikethrough': 's',
                'spoiler': 'tg-spoiler',
                'code': 'code',
                'pre': 'pre',
                'text_link': None}
        if entity.type not in tags.keys():
            continue
        #  right way to extract entity instead of obj.caption[entity.offset:entity.offset + entity.length:]
        pattern = entity.extract_from(new_message)
        shift_offset = new_message.index(pattern, int(entity.offset))

        if entity.type == 'text_link':
            new_pattern = f'<a href="{entity.url}">{pattern}</a>'
        else:
            new_pattern = f'<{tags.get(entity.type)}>{pattern}</{tags.get(entity.type)}>'

        before = new_message[:shift_offset]
        after = new_message[shift_offset + len(pattern):]  # shift + pattern length
        new_message = f'{before}{new_pattern}{after}'
    return new_message
