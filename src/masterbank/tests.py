from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from masterbank.models import MasterBank

class MasterBankModelTest(TestCase):

    def test_create_master_bank(self):
        # Given
        bank_code = "001"
        bank_name = "Test Bank"

        # When
        bank = MasterBank.objects.create(bank_code=bank_code, bank_name=bank_name)

        # Then
        self.assertEqual(bank.bank_code, bank_code)
        self.assertEqual(bank.bank_name, bank_name)

    def test_master_bank_str_method(self):
        # Given
        bank = MasterBank.objects.create(bank_code="002", bank_name="Another Bank")

        # When
        result = str(bank)

        # Then
        self.assertEqual(result, "Another Bank (002)")

    def test_unique_bank_code(self):
        # Given
        MasterBank.objects.create(bank_code="003", bank_name="Bank A")

        # When/Then
        with self.assertRaises(IntegrityError):
            MasterBank.objects.create(bank_code="003", bank_name="Bank B")

    def test_unique_bank_name(self):
        # Given
        MasterBank.objects.create(bank_code="004", bank_name="Unique Bank")

        # When/Then
        with self.assertRaises(IntegrityError):
            MasterBank.objects.create(bank_code="005", bank_name="Unique Bank")

    def test_max_length_bank_code(self):
        # Given
        long_code = "0" * 11  # 11 characters, which is more than the max_length

        # When
        bank = MasterBank(bank_code=long_code, bank_name="Long Code Bank")

        # Then
        with self.assertRaises(ValidationError):
            bank.full_clean()

    def test_max_length_bank_name(self):
        # Given
        long_name = "A" * 101  # 101 characters, which is more than the max_length

        # When
        bank = MasterBank(bank_code="007", bank_name=long_name)

        # Then
        with self.assertRaises(ValidationError):
            bank.full_clean()

    def test_create_multiple_banks(self):
        # Given/When
        bank1 = MasterBank.objects.create(bank_code="008", bank_name="Bank One")
        bank2 = MasterBank.objects.create(bank_code="009", bank_name="Bank Two")

        # Then
        self.assertEqual(MasterBank.objects.count(), 2)
        self.assertIn(bank1, MasterBank.objects.all())
        self.assertIn(bank2, MasterBank.objects.all())