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

LANGUAGE_CHOICE = Choices(
    ('en', 'English'),
    ('de', 'German'),
    ('pl', 'Polish'),
    ('ua', 'Ukrainian'),
)

COUNTRY_CHOICE = Choices(
    ('en', 'England'),
    ('de', 'Germany'),
    ('pl', 'Poland'),
    ('ua', 'Ukraine'),
)

PARTNER_TYPE_CHOICE = Choices(
    ('store', 'Store'),
    ('project', 'Project'),
)

WORK_TYPE_CATEGORY_CHOICE = Choices(
    ('tattoo', 'Tattoo'),
    ('piercing', 'Piercing'),
)
