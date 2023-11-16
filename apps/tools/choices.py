from model_utils import Choices


STATUS_CHOICES = Choices(
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('canceled', 'Canceled'),
    )


ROLE_CHOICES = Choices(
        ('master', 'Mater'),
        ('salon', 'Salon'),
    )
