from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0003_sellernotification"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "Pendiente"),
                    ("confirmed", "Confirmado"),
                    ("prepared", "Preparado"),
                    ("shipped", "Enviado"),
                    ("delivered", "Entregado"),
                    ("cancelled", "Cancelado"),
                ],
                default="pending",
                max_length=20,
            ),
        ),
    ]