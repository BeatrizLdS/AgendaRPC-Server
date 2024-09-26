from concurrent import futures
from repository import Repository
from model.agenda import Agenda
import gRPCModels.sync.agendas_sync_pb2 as sync_models
import gRPCModels.sync.agendas_sync_pb2_grpc as sync_grpc
import grpc
import google.protobuf.empty_pb2 as empty_pb2

def sync_agendas():
    repository = Repository.get_instace()
    local_agenda = repository.get_agenda()
    
    port_mapping = {
        'agenda1': 1203,
        'agenda2': 1204,
        'agenda3': 1205
    }
    
    for remote_agenda in Agenda.get_all_except(local_agenda):
        try:
            # Conecta com outras agendas
            channel = grpc.insecure_channel(f'localhost:{port_mapping[str(remote_agenda)]}')
            stub = sync_grpc.SyncAgendaServiceStub(channel)
            
            # Envia a lista de contatos da agenda local
            contacts = repository.get_all_sync()
            request = sync_models.SyncContactsList(contacts=contacts)
            response = stub.SyncAgendas(request)
            
            if response.isSuccess:
                print(f"Sincronização com {remote_agenda} foi bem-sucedida!")
            else:
                print(f"Falha ao sincronizar com {remote_agenda}: {response.description}")
            
        except Exception as e:
            print(f"Erro ao tentar sincronizar com {remote_agenda}")
            continue

def sync_with_other_agendas():
    repository = Repository.get_instace()
    local_agenda = repository.get_agenda()
    
    port_mapping = {
        'agenda1': 1203,
        'agenda2': 1204,
        'agenda3': 1205
    }
    
    for remote_agenda in Agenda.get_all_except(local_agenda):
        try:
            channel = grpc.insecure_channel(f'localhost:{port_mapping[str(remote_agenda)]}')
            stub = sync_grpc.SyncAgendaServiceStub(channel)
            response = stub.SyncFromOthers(empty_pb2.Empty())            
            repository.replace_all_with_sync(response)
            print(f"Sincronizado com sucesso da agenda {remote_agenda}.")
            break 
            
        except Exception as e:
            continue

class SyncAgendaService(sync_grpc.SyncAgendaServiceServicer):
    # TODO: FUnções para implementar
    # rpc SyncAgendas(SyncContactsList) returns (SyncResponse);
    # rpc SyncFromOthers(google.protobuf.Empty) returns (SyncContactsList);
    
    def SyncAgendas(self, request, context):
        print("Aqui é recebe a atualização que aconteceu em outra")
        repository = Repository.get_instace()
        local_agenda = repository.get_agenda()
        repository.replace_all_with_sync(request)
        response = sync_models.SyncResponse(isSuccess=True, description=f"{local_agenda} atualizada com sucesso!")
        return response
    
    def SyncFromOthers(self, request, context):
        repository = Repository.get_instace()
        contacts = repository.get_all_sync()
        response = sync_models.SyncContactsList(contacts=contacts)
        return response

def start_agenda_sync_server(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=100))
    sync_grpc.add_SyncAgendaServiceServicer_to_server(SyncAgendaService(), server)
    server.add_insecure_port(f'[::]:{port}')  # Usar a porta fornecida
    server.start()
    print(f"Server de sync iniciado e escutando na porta {port}")
    server.wait_for_termination()
