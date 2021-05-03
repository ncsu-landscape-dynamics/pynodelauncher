import subprocess
import sys

from mpi4py import MPI


def main():
    # MPI Initialization
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()
    debug = True

    if rank == 0:
        if len(sys.argv) != 2:
            sys.exit(f"Usage: {sys.argv[0]} filename")
        filename = sys.argv[1]

    if size == 1:
        sys.exit("Number of processes to run to be greater than 1")

    num_lines = 0
    if rank == 0:
        with open(filename) as task_file:
            lines = task_file.readlines()
        lines = [line for line in lines if line]  # skip empty lines
        num_lines = len(lines)
    num_lines = comm.bcast(num_lines, root=0)
    if rank == 0:
        if num_lines < size - 1:
            sys.exit(
                f"The number of provided commands ({num_lines}) is less"
                f" than the number of MPI worker tasks ({size - 1})"
            )
    else:
        if num_lines < size - 1:
            sys.exit()

    if rank == 0:
        pending_tasks = 0
        sent_tasks = 0

        # Read the rest, send after each read
        for i in range(1, size):
            line = lines[sent_tasks]
            comm.send(line, dest=i, tag=0)
            pending_tasks += 1
            sent_tasks += 1
            if debug:
                print(
                    f"pending tasks: {pending_tasks}, sent tasks {sent_tasks}"
                    f" (num_lines: {num_lines})"
                )
        # At this point, there is a task for each PE
        print(f"The first {size - 1} tasks have been sent")

        # Wait for results, which can be from any source.
        while True:
            status = MPI.Status()
            # TODO: Maybe this should be less aggressive in waiting and consume less CPU
            result = comm.recv(source=MPI.ANY_SOURCE, tag=0, status=status)
            # TODO: log the result
            free_proc = status.Get_source()  # Which PE is free to request a new task
            if debug:
                print(f"free_proc: {free_proc}")
            if sent_tasks < num_lines:
                line = lines[sent_tasks]
                print(f"Sending task {sent_tasks} of {num_lines}")
                comm.send(line, dest=free_proc, tag=0)
                sent_tasks += 1
            else:
                # All tasks have been sent - wait for all the results.
                pending_tasks -= 1
                print(f"Tasks left: {pending_tasks}")
            # If all the tasks are complete, exit.
            if pending_tasks == 0:
                break
        # When all the tasks are complete, tell the workers there will be no more
        # messages.
        for i in range(1, size):
            command = "QUIT"
            comm.send(command, dest=i, tag=0)
            print(f"Sent quit to PE {i}")
    else:
        while True:
            # Other processors receive inputs from proc0
            command = comm.recv(source=0, tag=0)
            if command == "QUIT":
                break
            completed_process = subprocess.run(command, shell=True, check=False)
            result = completed_process.returncode
            if debug:
                print(f"Called command from: {rank}")
                print(f"The command was: {command}")
            comm.send(result, dest=0, tag=0)


if __name__ == "__main__":
    main()
