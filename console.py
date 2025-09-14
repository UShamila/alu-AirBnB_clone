#!/usr/bin/python3
"""
Console module for the AirBnB clone project
"""
import cmd
import sys
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """
    Command interpreter class for the AirBnB clone
    """
    prompt = "(hbnb) "
    classes = {
        'BaseModel': BaseModel,
        'User': User,
        'State': State,
        'City': City,
        'Amenity': Amenity,
        'Place': Place,
        'Review': Review
    }

    def emptyline(self):
        """Do nothing when an empty line is entered"""
        pass

    def precmd(self, line):
        """Process the command line before execution"""
        # Handle empty lines and whitespace-only lines
        if not line or line.isspace():
            return ''
        return line

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program"""
        print()
        return True

    def help_quit(self):
        """Help for quit command"""
        print("Quit command to exit the program")

    def help_EOF(self):
        """Help for EOF command"""
        print("EOF command to exit the program")

    def do_create(self, arg):
        """Creates a new instance of BaseModel, saves it and prints the id"""
        if not arg:
            print("** class name missing **")
            return

        class_name = arg.split()[0]
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        new_instance = self.classes[class_name]()
        new_instance.save()
        print(new_instance.id)

    def do_show(self, arg):
        """Prints the string representation of an instance"""
        if not arg:
            print("** class name missing **")
            return

        args = arg.split()
        if len(args) < 1:
            print("** class name missing **")
            return

        class_name = args[0]
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        instance_id = args[1]
        key = f"{class_name}.{instance_id}"
        all_objects = storage.all()

        if key not in all_objects:
            print("** no instance found **")
            return

        print(all_objects[key])

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id"""
        if not arg:
            print("** class name missing **")
            return

        args = arg.split()
        if len(args) < 1:
            print("** class name missing **")
            return

        class_name = args[0]
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        instance_id = args[1]
        key = f"{class_name}.{instance_id}"
        all_objects = storage.all()

        if key not in all_objects:
            print("** no instance found **")
            return

        del all_objects[key]
        storage.save()

    def do_all(self, arg):
        """Prints all string representation of all instances"""
        all_objects = storage.all()
        result = []

        if not arg:
            for obj in all_objects.values():
                result.append(str(obj))
        else:
            class_name = arg.split()[0]
            if class_name not in self.classes:
                print("** class doesn't exist **")
                return

            for key, obj in all_objects.items():
                if key.startswith(f"{class_name}."):
                    result.append(str(obj))

        print(result)

    def do_update(self, arg):
        """Updates an instance based on the class name and id"""
        if not arg:
            print("** class name missing **")
            return

        args = arg.split()
        if len(args) < 1:
            print("** class name missing **")
            return

        class_name = args[0]
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        instance_id = args[1]
        key = f"{class_name}.{instance_id}"
        all_objects = storage.all()

        if key not in all_objects:
            print("** no instance found **")
            return

        if len(args) < 3:
            print("** attribute name missing **")
            return

        if len(args) < 4:
            print("** value missing **")
            return

        attr_name = args[2]
        attr_value = args[3]

        # Remove quotes if present
        if attr_value.startswith('"') and attr_value.endswith('"'):
            attr_value = attr_value[1:-1]

        # Cast to appropriate type
        obj = all_objects[key]
        if hasattr(obj, attr_name):
            attr_type = type(getattr(obj, attr_name))
            if attr_type == int:
                attr_value = int(attr_value)
            elif attr_type == float:
                attr_value = float(attr_value)
            # For string, keep as is

        setattr(obj, attr_name, attr_value)
        obj.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
