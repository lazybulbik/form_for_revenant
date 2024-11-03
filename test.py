from g4f import client
from g4f.models import gpt_4o_mini


promt_achievement = '''Твоя задача проанализировать текст и придумать Ачивку под текст. Учитывай, название и описание должны отражат черты человека, конкретно рассказчика.

В ответе предоставь Название (2-3 слова) и описание (6-10 слов) разделеных переносом строки без лишних комментариев. В ответе соблюдай правила и нормы русского языка.
Ответ должен быть с долей юмора.

Вот сообщение:
Я как-то купил хлеб, пока шел домой какой-то голубь подбежал и украл его'''
client = client.Client()
response = client.chat.completions.create(
    model=gpt_4o_mini,
    provider='Pizzagpt',
    messages=[
        {"role": "user", "content": promt_achievement},
    ]
    )
print(response.choices[0].message.content)