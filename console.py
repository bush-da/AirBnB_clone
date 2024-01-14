#!/usr/bin/python3
"""
Command interpreter module
"""
import cmd
from shlex import split
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models import storage


class HBNBCommand(cmd.Cmd):
    """
    Command interpreter class

    Attributes:
    - prompt (str): The custom prompt for the command interpreter.

    Methods:
    - do_quit(arg): Implements the 'quit' command to exit the program.
    - do_EOF(arg): Implements the 'EOF' command to exit the program.
    - emptyline(): Does nothing on an empty line.
    - do_create(arg): Creates a new instance of BaseModel or User, saves
      it (to the JSON file) and prints the id.
    - do_show(arg): Prints the string representation of an instance based
      on the class name and id.
    - do_destroy(arg): Deletes an instance based on the class name and id
      (saves the change into the JSON file)
    - do_all(arg): Prints all string representation of all instances based or
      not on the class name.
    - do_update(arg): Updates an instance based on the class name and id by
      adding or updating attribute (save the change into the JSON file).
    """

    prompt = "(hbnb) "
    class_mapping = {
            "BaseModel": BaseModel,
            "User": User,
            "Place": Place,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Review": Review,
        }

    def do_quit(self, arg):
        """
        Quit command to exit the program
        """
        if arg.strip() == "":
            return True
        print("** Invalid command for quit. Type 'quit' to exit.")
        return False

    def do_EOF(self, _):
        """
        EOF command to exit the program
        """
        print()
        return True

    def emptyline(self):
        """
        Do nothing on empty line
        """
        pass

    def do_create(self, arg):
        """
        Creates a new instance of BaseModel, User, Place, State, City,
        Amenity, or Review, saves it (to the JSON file) and prints the id.
        """
        args = split(arg)
        if not args or args[0] == "":
            print("** class name missing **")
            return

        try:
            class_name = args[0]
            new_instance = HBNBCommand.class_mapping[class_name]()
            new_instance.save()
            print(new_instance.id)
        except KeyError:
            print("** class doesn't exist **")
        except Exception as e:
            print("** {}".format(e))

    def do_show(self, arg):
        """
        Prints the string representation of an instance based
        on the class name and id.
        """
        args = split(arg)
        if not args or args[0] == "":
            print("** class name missing **")
            return
        try:
            class_name = args[0]

            if len(args) < 2:
                print("** instance id missing **")
                return

            instance_id = args[1]

            if class_name in HBNBCommand.class_mapping:
                class_type = HBNBCommand.class_mapping[class_name]
                instance_objects = [
                    obj for obj in storage.all().values()
                    if isinstance(obj, class_type) and obj.id == instance_id
                    ]
                if instance_objects:
                    print(instance_objects[0])
                else:
                    print("** no instance found **")
            else:
                print("** class doesn't exist **")

        except Exception as e:
            print("** {}".format(e))

    def do_destroy(self, arg):
        """
        Deletes an instance based on the class name and id
        (saves the change into the JSON file)
        """
        args = split(arg)
        if not args or args[0] == "":
            print("** class name missing **")
            return
        try:
            class_name = args[0]

            if len(args) < 2:
                print("** instance id missing **")
                return

            instance_id = args[1]
            key = "{}.{}".format(class_name, instance_id)
            obj = storage.all().get(key)
            if not obj:
                print("** no instance found **")
                return
            del storage.all()[key]
            storage.save()
        except Exception as e:
            print("** {}".format(e))

    def do_all(self, arg):
        """
        Prints all string representation of all instances based or
        not on the class name
        """
        args = split(arg)
        obj_list = []
        if not args or args[0] == "":
            for obj in storage.all().values():
                obj_list.append(str(obj))
            print(obj_list)
            return
        try:
            class_name = args[0]
            for obj in storage.all().values():
                if class_name == obj.__class__.__name__:
                    obj_list.append(str(obj))
            if not obj_list:
                print("** class doesn't exist **")
                return
            print(obj_list)
        except Exception as e:
            print("** {}".format(e))

    def do_update(self, arg):
        """
        Updates an instance based on the class name and id by adding
        or updating attribute (save the change into the JSON file).
        """
        args = split(arg)
        if not args or args[0] == "":
            print("** class name missing **")
            return
        try:
            class_name = args[0]

            if len(args) < 2:
                print("** instance id missing **")
                return

            instance_id = args[1]
            key = "{}.{}".format(class_name, instance_id)
            obj = storage.all().get(key)
            if not obj:
                print("** no instance found **")
                return
            if len(args) < 3:
                print("** attribute name missing **")
                return
            attribute_name = args[2]
            if len(args) < 4:
                print("** value missing **")
                return
            value = args[3]
            setattr(obj, attribute_name, value)
            obj.save()
        except Exception as e:
            print("** {}".format(e))

    def do_count(self, arg):
        """
        Retrieves the number of instances of a class.

        Usage:
            count <class name>
        """
        args = split(arg)
        if not args or args[0] == "":
            print("** class name missing **")
            return
        try:
            class_name = args[0]
            class_type = HBNBCommand.class_mapping.get(class_name)
            if not class_type:
                print("** class doesn't exist **")
                return
            count = sum(1 for obj in storage.all().values()
                        if isinstance(obj, class_type))
            print(count)
        except Exception as e:
            print("** {}".format(e))

    def do_help(self, arg):
        """
        Display help information for the available commands.

        Usage:
            help
            help <command>

        If no command is specified, it displays the list of
        documented commands.
        If a specific command is provided, it shows detailed
        help information for that command.

        Examples:
            help
            help quit

        Available Commands:
            EOF    - Exit the program
            help   - Display help information
            quit   - Quit the program
            create - Create a new instance and save it to the JSON file
            show   - Display the string representation of an instance
            destroy - Delete an instance based on the class name and id
            all    - Display string representations of all instances
            update - Update an instance based on the class name and id

        """
        if not arg:
            print("\nDocumented commands (type help <topic>):")
            print("========================================\n")
            for cmd_name in dir(self):
                if cmd_name.startswith("do_"):
                    command = cmd_name[3:]
                    docstring = getattr(self, cmd_name).__doc__.strip()
                    print(f"{command}: {docstring}\n")
        else:
            cmd_method = getattr(self, f"do_{arg}", None)
            if cmd_method:
                print(f"Help for {arg}:")
                print(cmd_method.__doc__)
            else:
                print(f"** No help available for {arg} **")

    def default(self, line):
        """
        Handles calss name followed by an argument.
        eg: <class_name>.all()
        """
        args = line.split('.')
        class_arg = args[0]
        if len(args) == 1:
            print("*** Unknown syntax: {}".format(line))
            return
        try:
            args = args[1].split("(")
            command = args[0]
            if command == "all":
                HBNBCommand.do_all(self, class_arg)
            elif command == "count":
                HBNBCommand.do_count(self, class_arg)
            elif command == "show":
                args = args[1].split(')')
                id_arg = args[0]
                id_arg = id_arg.strip("'")
                id_arg = id_arg.strip('"')
                arg = class_arg + ' ' + id_arg
                HBNBCommand.do_show(self, arg)
            elif command == "destroy":
                args = args[1].split(')')
                id_arg = args[0]
                id_arg = id_arg.strip('"')
                id_arg = id_arg.strip("'")
                arg = class_arg + ' ' + id_arg
                HBNBCommand.do_destroy(self, arg)
            elif command == 'update':
                args = args[1].split(',')
                id_arg = args[0].strip("'")
                id_arg = id_arg.strip('"')
                name_arg = args[1].strip(',')
                val_arg = args[2]
                name_arg = name_arg.strip(' ')
                name_arg = name_arg.strip("'")
                name_arg = name_arg.strip('"')
                val_arg = val_arg.strip(' ')
                val_arg = val_arg.strip(')')
                arg = class_arg + ' ' + id_arg + ' ' + name_arg + ' ' + val_arg
                HBNBCommand.do_update(self, arg)
            else:
                print("*** Unknown syntax: {}".format(line))
        except IndexError:
            print("*** Unknown syntax: {}".format(line))


if __name__ == '__main__':
    HBNBCommand().cmdloop()
