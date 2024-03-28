if [ ! -f .env ]
then
  export $(cat .env | xargs)
fi

cat <<EOF | python manage.py shell
from django.contrib.auth import get_user_model

User = get_user_model()  # get the currently active user model,

user = os.getenv('DJANGO_SUPERUSER_USERNAME')
email = os.getenv('DJANGO_SUPERUSER_EMAIL')
password = os.getenv('DJANGO_SUPERUSER_PASSWORD')

User.objects.filter(username=user).exists() or \
    User.objects.create_superuser(user, email, password)
EOF