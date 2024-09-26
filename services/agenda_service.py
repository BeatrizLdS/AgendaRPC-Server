import grpc
from concurrent import futures

import gRPCModels.agenda.agenda_pb2_grpc as agenda_service
import gRPCModels.agenda.agenda_pb2 as agenda_models
from repository import Repository

class AgendaService(agenda_service.AgendaService):
    # TODO: Funções para serem implementadas:
    # rpc CheckConnection(Empty) returns (Response) {};
    # rpc GetAllContacts(Empty) returns (ContactsList) {};
    # rpc AddContact(Contact) returns (Response) {};
    # rpc RemoveContact(Contact) returns (Response) {};
    # rpc UpdateContact(Contact) returns (Response) {};
    
    def CheckConnection(self, request, context):
        response = agenda_models.Response(isSuccess=True, description="Conexão estabelecida com sucesso!")
        return response
    
    def GetAllContacts(self, request, context):
        repository = Repository.get_instace()
        contacts = repository.get_all()
        return agenda_models.ContactsList(contacts=list(contacts))
    
    def AddContact(self, contact, context):
        repository = Repository.get_instace()
        result = repository.add_contact(contact)
        if result:
            response = agenda_models.Response(isSuccess=True, description="Contato adicionado com sucesso")
            return response 
        response = agenda_models.Response(isSuccess=False, description="Contato já existente")
        return response
    
    def RemoveContact(self, contact, context):
        repository = Repository.get_instace()
        result = repository.remove_contact(contact)
        if result:
            response = agenda_models.Response(isSuccess=True, description="Contato removido com sucesso")
            return response
        response = agenda_models.Response(isSuccess=False, description="Contato não existente para ser removido")
        return response
    
    def UpdateContact(self, contact, context):
        repository = Repository.get_instace()
        result = repository.update_contact(contact)
        if result:
            response = agenda_models.Response(isSuccess=True, description="Contato atualizado com sucesso")
            return response
        response = agenda_models.Response(isSuccess=False, description="Contato não existente para ser atualizado")
        return response
    
def start_agenda_server(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=100))
    agenda_service.add_AgendaServiceServicer_to_server(AgendaService(), server)
    server.add_insecure_port(f'[::]:{port}')  # Usar a porta fornecida
    server.start()
    print(f"Server iniciado e escutando na porta {port}")
    server.wait_for_termination()
    