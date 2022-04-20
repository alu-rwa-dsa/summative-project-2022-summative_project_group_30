import multiprocessing
from configs.db_conn import connect_db

if __name__ == '__main__':
    connect_db()
    from Backend.main import run_api
    from Frontend.login import login_window

    Process_jobs = [run_api, login_window]
    P = []
    for process in Process_jobs:
        p = multiprocessing.Process(target=process)
        p.start()
        P.append(p)

    for p in P:
        p.join()
