from django.test import TestCase
from contacts.models import Contact
import datetime

class ContactTestCase(TestCase):
    def setUp(self):
        Contact.objects.create(code="000000001", birthday=datetime.date(1983,9,24))
        Contact.objects.create(code="000000002", birthday=datetime.date(1945,5,9))