from rest_framework.serializers import ValidationError
import re


class TelegramIdValidator:
    """Валидатор для Telegram ID"""

    def __call__(self, value):
        if value is None:
            return value

        # Telegram ID должен содержать только цифры и быть не короче 5 символов
        if not re.match(r"^\d{5,}$", str(value)):
            raise ValidationError(
                "Telegram ID должен содержать только цифры и быть не короче 5 символов."
            )

        # Проверка максимальной длины
        if len(str(value)) > 50:
            raise ValidationError("Telegram ID не может превышать 50 символов.")

        return value


class EmailValidator:
    """Валидатор для email"""

    def __call__(self, value):
        if not value:
            raise ValidationError("Email является обязательным полем.")

        # Базовая проверка формата email
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_regex, value):
            raise ValidationError("Введите корректный email адрес.")

        # Проверка максимальной длины (EmailField обычно ограничен 254 символами)
        if len(value) > 254:
            raise ValidationError("Email не может превышать 254 символа.")

        return value


class FirstNameValidator:
    """Валидатор для имени"""

    def __call__(self, value):
        if not value:
            raise ValidationError("Имя является обязательным полем.")

        # Проверка длины
        if len(value) > 50:
            raise ValidationError("Имя не может превышать 50 символов.")

        # Проверка на допустимые символы (только буквы, пробелы и дефисы)
        if not re.match(r"^[a-zA-Zа-яА-ЯёЁ\s\-]+$", value):
            raise ValidationError("Имя может содержать только буквы, пробелы и дефисы.")

        return value


class LastNameValidator:
    """Валидатор для фамилии"""

    def __call__(self, value):
        # Фамилия может быть пустой
        if not value:
            return value

        # Проверка длины
        if len(value) > 50:
            raise ValidationError("Фамилия не может превышать 50 символов.")

        # Проверка на допустимые символы (только буквы, пробелы и дефисы)
        if not re.match(r"^[a-zA-Zа-яА-ЯёЁ\s\-]+$", value):
            raise ValidationError(
                "Фамилия может содержать только буквы, пробелы и дефисы."
            )

        return value
