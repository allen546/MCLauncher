import os
import os.path


class Command():
    def __init__(self, executable, args, kwargs):
        """
        Represents a command.
        :executable is the executable in question

        :args is a list of args, like in:
            python3 --version
        :args would be ["--version",]

        :kwargs is a dict of args, like in:
            python3 -c "test"
        :kwargs would be {"-c": "\"test\""}
        this is for the sake of clarity, not nessecary

        Methods:
        build(self) -> str - constructs and returns the command 

        get_value_for(self, key) -> str - returns the value of kwargs[attr]

        setvalue(self, key, value) -> None - adds an entry to kwargs

        add_arg(self, arg) -> None - adds an entry to args
        """
        self.exe = executable
        self.args = list(args)
        self.kwargs = dict(kwargs)

    def build(self):
        cmd = [os.path.abspath(os.path.expanduser(cmd))]
        for arg in self.args:
            cmd.append(arg)

        for key, value in self.kwargs:
            cmd.append(key)
            cmd.append(str(value))

        return cmd
    
    def get_value_for(self, key):
        try:
            return self.kwargs[key]
        except KeyError:
            return None
        

    def setvalue(self, key, value):
        self.kwargs[key] = value

    def add_arg(self, arg):
        self.args.append(arg)
    
