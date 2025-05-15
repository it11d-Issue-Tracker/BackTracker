# Issue_Tracker/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db import connection
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=User)
def sync_auth_user_to_users(sender, instance, created, **kwargs):
    """
    Sincronitza la taula auth_user amb la taula users.
    """
    with connection.cursor() as cursor:
        if created:
            # Inserir un nou registre a la taula users
            cursor.execute(
                """
                INSERT INTO perfils (id_user, username)
                VALUES (%s, %s)
                """,
                [instance.id, instance.username]
            )
            Token.objects.create(user=instance)

        else:
            # Actualitzar un registre existent a la taula users
            cursor.execute(
                """
                UPDATE perfils
                SET username = %s
                WHERE id_user = %s
                """,
                [instance.username, instance.id]
            )