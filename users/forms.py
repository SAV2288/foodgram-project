from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


User = get_user_model()


class CreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs.update({"id": "id_first_name", "class": "form__input"})
        self.fields["last_name"].widget.attrs.update({"id": "id_last_name", "class": "form__input"})
        self.fields["username"].widget.attrs.update({"id": "id_username", "class": "form__input"})
        self.fields["email"].widget.attrs.update({"id": "id_email", "class": "form__input"})
        self.fields["password1"].widget.attrs.update({"id": "id_password", "class": "form__input"})
        self.fields["password2"].widget.attrs.update({"id": "id_password", "class": "form__input"})


    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("first_name", "last_name", "username", "email")
        labels = {
            "first_name": "Имя",
            "last_name": "Фамилия",
            "username": "Имя пользователя",
            "email": "Адрес электронной почты",
            "password1": "Пароль",
            "password2": "Подтвердить пароль",
        }