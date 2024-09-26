class Contact:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone

    def __eq__(self, other):
        if isinstance(other, Contact):
            return self.name == other.name
        return False

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return f"Nome:{self.name}\n Número:{self.phone}"

    def __repr__(self):
        return f"Contact(name={self.name}, phone_phone={self.phone})"
