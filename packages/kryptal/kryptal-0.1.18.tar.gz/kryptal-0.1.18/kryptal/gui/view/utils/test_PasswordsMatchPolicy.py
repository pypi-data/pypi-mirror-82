from PyQt5.QtWidgets import QLineEdit, QWidget  # type: ignore
from kryptal.gui import Application
from kryptal.gui.view.utils.PasswordsMatchPolicy import display
from kryptal.testutils.ApplicationHelpers import with_app
import unittest


class test_PasswordsMatchPolicy(unittest.TestCase):
    def setUp(self) -> None:
        self.indicator = QWidget()
        self.password1Field = QLineEdit()
        self.password2Field = QLineEdit()

    @with_app
    def test_is_initially_not_shown_when_fields_equal(self) -> None:
        self.password1Field.setText("")
        self.password2Field.setText("")
        display(self.indicator).whenPasswordsDontMatch(
            [self.password1Field, self.password2Field])
        self.assertFalse(self.indicator.isVisible())

    @with_app
    def test_is_initially_shown_when_fields_not_equal(self) -> None:
        self.password1Field.setText("pw1")
        self.password2Field.setText("pw2")
        display(self.indicator).whenPasswordsDontMatch(
            [self.password1Field, self.password2Field])
        self.assertTrue(self.indicator.isVisible())

    @with_app
    def test_changes_to_shown_when_fields_unequal_change1st(self) -> None:
        self.password1Field.setText("")
        self.password2Field.setText("")
        display(self.indicator).whenPasswordsDontMatch(
            [self.password1Field, self.password2Field])
        self.assertFalse(self.indicator.isVisible())
        self.password1Field.setText("different")
        self.assertTrue(self.indicator.isVisible())

    @with_app
    def test_changes_to_shown_when_fields_unequal_change2nd(self) -> None:
        self.password1Field.setText("")
        self.password2Field.setText("")
        display(self.indicator).whenPasswordsDontMatch(
            [self.password1Field, self.password2Field])
        self.assertFalse(self.indicator.isVisible())
        self.password2Field.setText("different")
        self.assertTrue(self.indicator.isVisible())

    @with_app
    def test_changes_to_not_shown_when_fields_equal_change1nd(self) -> None:
        self.password1Field.setText("pw1")
        self.password2Field.setText("pw2")
        display(self.indicator).whenPasswordsDontMatch(
            [self.password1Field, self.password2Field])
        self.assertTrue(self.indicator.isVisible())
        self.password2Field.setText("pw1")
        self.assertFalse(self.indicator.isVisible())

    @with_app
    def test_changes_to_not_shown_when_fields_equal_change2nd(self) -> None:
        self.password1Field.setText("pw1")
        self.password2Field.setText("pw2")
        display(self.indicator).whenPasswordsDontMatch(
            [self.password1Field, self.password2Field])
        self.assertTrue(self.indicator.isVisible())
        self.password1Field.setText("pw2")
        self.assertFalse(self.indicator.isVisible())


class test_PasswordsMatchPolicy_2(unittest.TestCase):
    @with_app
    def test_zero_password_fields(self) -> None:
        indicator = QWidget()
        display(indicator).whenPasswordsDontMatch([])
        self.assertFalse(indicator.isVisible())

    @with_app
    def test_one_password_fields(self) -> None:
        indicator = QWidget()
        passwordField = QLineEdit()
        passwordField.setText("sometext")
        display(indicator).whenPasswordsDontMatch([passwordField])
        self.assertFalse(indicator.isVisible())
