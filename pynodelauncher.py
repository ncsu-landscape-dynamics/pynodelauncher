import argparse
import subprocess
import sys

from mpi4py import MPI


def print_message(*args, **kwargs):
    """Print informative message"""
    print(*args, **kwargs, flush=True)


def print_error(*args, **kwargs):
    """Print error message"""
    print(*args, **kwargs, file=sys.stderr, flush=True)


def cli_parser():
    """Create CLI parser"""
    parser = argparse.ArgumentParser(description="Launch subprocesses using MPI")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="output more messages about the task scheduling",
    )
    parser.add_argument("file", help="file with list of tasks (commands to execute)")
    return parser


def main():
    # MPI Initialization
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()
    verbose = False

    if rank == 0:
        args = cli_parser().parse_args()
        filename = args.file
        verbose = args.verbose

    verbose = comm.bcast(verbose, root=0)

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
            if verbose:
                print_message(
                    f"Pending tasks: {pending_tasks}, sent tasks: {sent_tasks}"
                    f" (from total: {num_lines})"
                )
        # At this point, there is a task for each PE
        print_message(
            f"The first {sent_tasks} tasks have been sent,"
            f" {num_lines - sent_tasks} are queued"
        )

        # Wait for results, which can be from any source.
        while True:
            status = MPI.Status()
            # TODO: Maybe this should be less aggressive in waiting and consume less CPU
            result = comm.recv(source=MPI.ANY_SOURCE, tag=0, status=status)
            free_proc = status.Get_source()  # Which PE is free to request a new task
            if verbose:
                print_message(f"Worker {free_proc} finished its task")
            if sent_tasks < num_lines:
                line = lines[sent_tasks]
                comm.send(line, dest=free_proc, tag=0)
                sent_tasks += 1
                print_message(f"Sent task {sent_tasks} of {num_lines}")
            else:
                # All tasks have been sent - wait for all the results.
                pending_tasks -= 1
                print_message(f"Tasks still running: {pending_tasks}")
            # If all the tasks are complete, exit.
            if pending_tasks == 0:
                break
        # When all the tasks are complete, tell the workers there will be no more
        # messages.
        for i in range(1, size):
            command = "QUIT"
            comm.send(command, dest=i, tag=0)
            print_message(f"Sent quit message to worker {i}")
    else:
        while True:
            # Other processors receive inputs from proc0
            command = comm.recv(source=0, tag=0)
            if command == "QUIT":
                break
            # No security concern here. The point is to execute arbitrary user code.
            completed_process = subprocess.run(
                command, shell=True, check=False
            )  # nosec
            result = completed_process.returncode
            if result:
                print_error(
                    f"Command ended with non-zero return code {result}: {command}"
                )
            if verbose:
                print_message(f"Worker {rank} completed command: {command}")
            comm.send(result, dest=0, tag=0)


if __name__ == "__main__":
    main()
