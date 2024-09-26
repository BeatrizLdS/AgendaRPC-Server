import grpc
import google.protobuf.empty_pb2 as empty_pb2
from concurrent import futures
from repository import Repository
from model.agenda import Agenda
import gRPCModels.sync.agendas_sync_pb2 as sync_models
import gRPCModels.sync.agendas_sync_pb2_grpc as sync_grpc

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
            print(f"Erro ao tentar sincronizar com {remote_agenda}: {e}")
            continue

def sync_with_other_agendas():
    print("Entrou para executar o sync self")
    """ Lógica para sincronizar com outras agendas fora do contexto gRPC """
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
            print(f"Erro ao tentar sincronizar com {remote_agenda}: {e}")
            continue

class SyncAgendaService(sync_grpc.SyncAgendaServiceServicer):
    # TODO: FUnções para implementar
    # rpc SyncAgendas(SyncContactsList) returns (SyncResponse);
    # rpc SyncFromOthers(google.protobuf.Empty) returns (SyncContactsList);
    
    def SyncAgendas(self, request, context):
        print("Aqui é a que recebe de outra")
        return super().SyncAgendas(request, context)
    
    def SyncFromOthers(self, request, context):
        print("Ta peganso as informações")
        return sync_models.SyncContactsList()

def start_agenda_sync_server(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=100))
    sync_grpc.add_SyncAgendaServiceServicer_to_server(SyncAgendaService(), server)
    server.add_insecure_port(f'[::]:{port}')  # Usar a porta fornecida
    server.start()
    print(f"Server de sync iniciado e escutando na porta {port}")
    server.wait_for_termination()
