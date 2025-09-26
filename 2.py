# Шаблон - класс
class Phone:
    def __init__(self, year, color, brand,cameras,connector,display):
        self.year = year
        self.color = color
        self.brand = brand
        self.cameras = cameras
        self.connector = connector
        self.display = display

    # Метод
    def info(self):
        # self - ссылка на объект, у которого вызвали метод
        print("Бренд телефона", self.brand, "цвет", self.color, "год", self.year, "камеры", self.cameras, "разъем", self.connector, "дисплей", self.display)

# Объект - машины на основе класса (шаблона) Car

phone = Phone(color = "титановый", brand = "айфон",year = 2024,cameras = 3,connector = "lightning",display = "OLED")
phone1 = Phone(color = "зеленый", brand = "самсунг",year = 2025,cameras = 2,connector = "usb type-c 3.0",display = "AMOLED")
phone2 = Phone(color = "желтый",brand = "поко",year = 2023,cameras = 1,connector = "usb type-c 3.0",display = "AMOLED")


# Вызываем метод info у объекта car1
# Программа сама выставит self на car1
phone.info()
phone1.info()
phone2.info()

