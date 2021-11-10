# необходимо ввести свой свой логин и пароль для авторизации
# либо задать массив с пулом аккунтов
login = ''
password = ''





import vk_api
import sys
import numpy as np
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModelWithLMHead

# tokenizer = AutoTokenizer.from_pretrained("ctrl")
# model = AutoModelForCausalLM.from_pretrained("ctrl")

tokenizer = AutoTokenizer.from_pretrained("sberbank-ai/rugpt3large_based_on_gpt2")
model = AutoModelWithLMHead.from_pretrained("sberbank-ai/rugpt3large_based_on_gpt2")

def gen_comment(input_context, size):
    input_ids = tokenizer(input_context, return_tensors="pt").input_ids
    outputs = model.generate(input_ids=input_ids, max_length=size, repetition_penalty=1.2)
    comment = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return comment

def add_comment(owner_id, post_id, input_ids):
    comment = gen_comment(input_ids, 20)
    vk.method('wall.createComment', {
        'owner_id': owner_id,
        'post_id': post_id,
        'message': comment,
    })

def add_post(owner_id, input_ids):
    comment = gen_comment(input_ids, 100)
    vk.method('wall.post', {
        'owner_id': owner_id,
        'message': comment,
    })

def vk_auth(login, password):
    vk = vk_api.VkApi(login, password)
    try:
        vk.auth()  # Авторизируемся
    except vk_api.AuthorizationError as error_msg:
        print(error_msg)
        sys.exit()
    return vk

# Авторизируемся
vk = vk_auth(login, password)

#добавление поста
owner_id = -200726934 # group id in database vk
topics = ['Событие года', 'Авария', 'Власти Москвы', 'Новое открытие в науке', 'OpenAI новая модель gpt3', 'Увеличили налоги', 'Повысили зарплаты', 'Раскрыто преступление', 'Скоро Новый Год', 'Презентация новой технологии', 'В конце декабря в отпуск']
[ add_post(owner_id, topic) for topic in topics ]

# добавление комментариев под постом на стене пользователя
# user_id = 190905742
# post_id = 1688
user_id = -200726934
# post_id = 6
# num_comments = 100
# [add_comment(user_id, post_id, 'Неплохо') for i in range(num_comments)]
# add_comment(user_id, post_id, 'Мне страшно')
posts_id = [np.random.randint(13,23) for _ in range(11) ]
comments = [ 'согласен', 'Плохая идея', 'Ерунда', 'Звучит неплохо', 'ужас', 'какой кошмар', 'не доказательно', 'нет мыслей по этому поводу', 'хорошее качество', 'интересно', 'познавательно' ]
[add_comment(user_id, post_id, comment) for post_id, comment in zip(posts_id, comments)]



