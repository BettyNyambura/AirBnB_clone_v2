import unittest
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand
from models import storage
from models.user import User


class TestDoCreate(unittest.TestCase):
    """Test the do_create method of HBNBCommand"""

    def setUp(self):
        """Set up test environment"""
        self.console = HBNBCommand()

    def tearDown(self):
        """Clean up after tests"""
        # Delete all objects created during tests
        all_objs = storage.all()
        for key in list(all_objs.keys()):
            del all_objs[key]
        storage.save()

    def test_create_missing_class_name(self):
        """Test create with no class name"""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.do_create("")
            self.assertEqual(
                    fake_out.getvalue().strip(), "** class name missing **"
            )

    def test_create_nonexistent_class(self):
        """Test create with a nonexistent class name"""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.do_create("NonExistentClass")
            self.assertEqual(
                    fake_out.getvalue().strip(), "** class doesn't exist **"
            )

    def test_create_with_no_params(self):
        """Test create with only class name"""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.do_create("User")
            output = fake_out.getvalue().strip()
            obj_key = f"User.{output}"
            self.assertIn(obj_key, storage.all())

    def test_create_with_valid_params(self):
        """Test create with valid parameters"""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.do_create(
                    'User name="John_Doe" age=30 height=5.9'
            )
            output = fake_out.getvalue().strip()
            obj_key = f"User.{output}"
            self.assertIn(obj_key, storage.all())
            user = storage.all()[obj_key]
            self.assertEqual(user.name, "John Doe")
            self.assertEqual(user.age, 30)
            self.assertEqual(user.height, 5.9)

    def test_create_with_invalid_params(self):
        """Test create with some invalid parameters"""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.do_create(
                    'User name="Jane_Doe" age=twenty height=5.8'
            )
            output = fake_out.getvalue().strip()
            obj_key = f"User.{output}"
            self.assertIn(obj_key, storage.all())
            user = storage.all()[obj_key]
            self.assertEqual(user.name, "Jane Doe")
            self.assertFalse(hasattr(user, 'age'))
            self.assertEqual(user.height, 5.8)

    def test_create_with_escaped_quotes(self):
        """Test create with escaped quotes in string"""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.do_create(
                    'User bio="Loves \\"coding\\" and hiking"'
            )
            output = fake_out.getvalue().strip()
            obj_key = f"User.{output}"
            self.assertIn(obj_key, storage.all())
            user = storage.all()[obj_key]
            self.assertEqual(user.bio, 'Loves "coding" and hiking')


if __name__ == '__main__':
    unittest.main()
