import services.agenda_service as agenda_service
import services.sync_agendas_service as sync_service
import repository
import threading  
import sys  
from model.agenda import Agenda

def main():
    agenda = None
    if len(sys.argv) < 2:
        print("Insira uma agenda válida \nAgendas válidas: agenda1, agenda2, agenda3")
        return
    else:
        agenda_name = sys.argv[1]
        agenda = Agenda.get_by_name(agenda_name)
        if agenda is None:
            print("Insira uma agenda válida \nAgendas válidas: agenda1, agenda2, agenda3")
            return
        
    repository.Repository(agenda)
     
    port_mapping = {
        'agenda1': 1200,
        'agenda2': 1201,
        'agenda3': 1202
    }
    
    port_sync_mapping = {
        'agenda1': 1203,
        'agenda2': 1204,
        'agenda3': 1205
    }
    
    port = port_mapping.get(agenda_name, 1200)
    port_sync = port_sync_mapping.get(agenda_name, 1200)
        
        
    agenda_thread = threading.Thread(target=agenda_service.start_agenda_server, args=(port,))
    agenda_thread.start()
    
    # Realizar a sincronização automática com outras agendas, similar ao syncSelf do Java
    sync_thread = threading.Thread(target=sync_service.start_agenda_sync_server, args=(port_sync,))
    sync_thread.start()
        
    print(f"{agenda} está sendo executada...")
    sync_service.sync_with_other_agendas()
    
    agenda_thread.join()
    sync_thread.join()
    
    

if __name__ == '__main__':
    main()
    
    
    
    