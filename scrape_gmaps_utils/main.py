from bose.launch_tasks import launch_tasks
from bose import LocalStorage
from src import tasks_to_be_run

msg = 'Done....'

def print_msg():
    global msg
    print(msg) 

if __name__ == "__main__":

    launch_tasks(*tasks_to_be_run)
    count = LocalStorage.get_item('count', 0)
    
    print_msg()
