import threading


class ParallelJob:

    def __init__(self, max_job):
        self.max_job = max_job
        self.threads = {}
        self.non_started = []

    def append_job(self, process, args, thread_id):
        new_thread = threading.Thread(target=process, args=args, name=f"Thread-{thread_id}")
        self.threads[thread_id] = new_thread
        self.non_started.append(new_thread)

    def start_threads(self):
        for thread in self.non_started:
            thread.start()
        self.non_started = []

    def wait_all_jobs(self):
        while self.threads.values():
            pass
        self.threads = {}

    def is_possible_new_job(self):
        return len(self.threads) < self.max_job

    def remove_thread(self, thread_id):
        self.threads.pop(thread_id)