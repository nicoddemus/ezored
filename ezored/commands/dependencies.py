"""Dependencies command."""


from .base import Base


class Dependencies(Base):

    def run(self):
        print("Dependencies!")

        if self.options["update"]:
            self.update()

    def update(self):
        print("Updating!!!")
