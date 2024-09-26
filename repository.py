import gRPCModels.agenda.agenda_pb2 as agenda_models
import gRPCModels.sync.agendas_sync_pb2 as sync_models
from model.contact import Contact
from typing import List, Set

class Repository:
    _instance = None
    
    def __new__(cls, agenda=None):
        if cls._instance is None and agenda is not None:
            cls._instance = super(Repository, cls).__new__(cls)
            cls._instance.init(agenda)
        return cls._instance
    
    def init(self, agenda):
        self._agenda = agenda
        self.contacts = set()
        
    def get_agenda(self):
        return self._agenda
    
    @classmethod
    def get_instace(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def add_contact(self, contact):
        newContact = Contact(contact.name, contact.phone)
        exists = newContact in self.contacts
        if exists == False:
            self.contacts.add(newContact)
            return True
        return False
        
    def remove_contact(self, contact):
        appContact = self.convert_protobuf_to_app_contact(contact)    
        if appContact in self.contacts:
            self.contacts.remove(appContact)
            return True
        return False
    
    def convert_app_contact_to_sync_protobuf(self, contact: Contact) -> sync_models.SyncContact:
        return sync_models.SyncContact(
            name=contact.name,
            phone=contact.phone
        )
        
    def convert_sync_protobuf_to_app_contact(self, contact: sync_models.SyncContact) -> Contact:
        return Contact(
            name=contact.name,
            phone=contact.phone
    )
    
    def convert_app_contact_to_protobuf(self, contact: Contact) -> agenda_models.Contact:
        return agenda_models.Contact(
            name=contact.name,
            phone=contact.phone
        )
        
    def convert_protobuf_to_app_contact(self, contact: agenda_models.Contact) -> Contact:
        return Contact(
            name=contact.name,
            phone=contact.phone
    )

    def get_all(self):
        returnList = [self.convert_app_contact_to_protobuf(contact) for contact in self.contacts]
        return returnList
    
    def get_all_sync(self):
        returnList = [self.convert_app_contact_to_sync_protobuf(contact) for contact in self.contacts]
        return returnList
    
    def replace_all_with_sync(self, contacts):
        newList = [self.convert_sync_protobuf_to_app_contact(contact) for contact in contacts.contacts]
        self.contacts = newList
    
    def update_contact(self, contact):
        appContact = self.convert_protobuf_to_app_contact(contact)   
        for existing_contact in self.contacts:
            if existing_contact == appContact:
                self.contacts.remove(existing_contact)
                self.contacts.add(appContact)
                return True
        return False
        
    
