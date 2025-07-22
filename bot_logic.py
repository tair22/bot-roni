import random, time, requests

def gen_pass(pass_length):
    elements = "+-/*!&$#?=@<>123456789"
    password = ""

    for i in range(pass_length):
        password += random.choice(elements)

    return password

def gen_emodji():
    emodji = ["\U0001f600", "\U0001f642", "\U0001F606", "\U0001F923", "\U0001FA84", "\U0001F3AE", "\U0001F579", "\U0001F3B0", "\U0001F9BB", "\U0001F443", "\U0001F9E0", "\U0001FAC0", "\U0001FAC1", "\U0001F9B7"]
    return random.choice(emodji)


def flip_coin():
    flip = random.randint(0, 2)
    if flip == 0:
        return ("Решка")
    else:
        return ("Орёл")


def jokes():
    jokes = [ "- Изя, ну что там?!"
    "- Наши таки побеждают.."
    "- А наши это кто? "
    "- Таки скоро узнаем...", "— Здравствуйте, а кем вы работаете?"
    "— Я аудитор."
    "— Ха-ха-ха, а я тогда бмветор."
    , "В свете последних событий обезьяны начали отрицать, что они наши предки.", 
    "Сидит лось на рельсах. К нему подходит другой лось и говорит:"
    "-Подвинься", 
    "Экстренные новости:"
    "Полиция задержала дерево. По их словам, у задержанного был ствол. При обыске нашли шишки"]
    return random.choice(jokes)


def timers():
    timer = time.ctime()
    return (timer)


def get_duck_image_url():    
        url = 'https://random-d.uk/api/random'
        res = requests.get(url)
        data = res.json()
        return data['url']

def get_dog_image_url():    
        url = ' https://random.dog/woof.json'
        res = requests.get(url)
        data = res.json()
        return data['url']


    

    




    
    