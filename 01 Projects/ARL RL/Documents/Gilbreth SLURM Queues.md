## Introduction to SLURM and Queues

The **Simple Linux Utility for Resource Management (SLURM)** is a system for managing and scheduling jobs on compute clusters like Gilbreth. When you submit a job, you're essentially asking SLURM to allocate resources (like GPUs, CPUs, and memory) for your task. Your job is placed in a **queue**, and SLURM will execute it when the requested resources become available. On Gilbreth, the concepts of **Partitions**, **Accounts**, and **Quality of Service (QOS)** are crucial for understanding how queues work.

---

## Job Submission on Gilbreth

A typical job submission command on Gilbreth has four main parts. Here is an example:

Bash

```
sbatch --ntasks=1 --gpus-per-task=1 --cores-per-task=4 --mem=50G --partition=a100-40gb --account=rcac --qos=standby
```

- `--partition`: Specifies the group of nodes you want to run your job on.
    
- `--account`: Similar to a queue, you need to specify which account your job should be charged to.
    
- `--qos`: Determines the priority and policies for your job.
    

---

## Partitions

On Gilbreth, different types of nodes are organized into distinct **partitions**. This allows for separate charging and management of resources. You must specify a partition when submitting a job.

### V100 Partition

- **Nodes**: This partition contains 14 Gilbreth-E nodes and 5 Gilbreth-F nodes.
    
- **Hardware**: Each node has NVIDIA V100 GPUs with either 16GB or 32GB of memory and 190GB of CPU memory.
    
- **Submission**: To submit to this partition, use `-p v100` or `--partition=v100`.
    
- **Constraint**: If your job requires more than 16GB of GPU memory, you must specify the constraint `--constraint=v100-32gb` to ensure your job runs on a Gilbreth-F node.
    

### A30 Partition

- **Nodes**: This partition is made up of 16 Gilbreth-B nodes and 8 Gilbreth-D nodes.
    
- **Hardware**: Each node contains three NVIDIA A30 GPUs, each with 24GB of memory.
    

### Other Partitions

The search results also mention other node types that are likely in their own partitions:

- **Gilbreth-C nodes**: 4 NVIDIA V100s
    
- **Gilbreth-J nodes**: 4 NVIDIA A100s
    
- **Gilbreth-l nodes**: 4 NVIDIA H100s
    

---

## Accounts

In the SLURM environment on Gilbreth, an "Account" is what you might traditionally think of as a queue. To see which accounts are available to you, use the `slist` command. The `standby` account is available to everyone on Gilbreth.

---

## Quality of Service (QOS)

The **Quality of Service (QOS)** setting for your job affects its priority and the policies applied to it.

### `normal` QOS

- **Priority**: High priority, with a short expected wait time.
    
- **Resource Allocation**: GPUs requested by these jobs are withdrawn from the account until the job finishes.
    
- **Job Duration**: Can run for up to two weeks.
    

### `standby` QOS

- **Priority**: Low priority, with no guaranteed start time. Jobs may take hours or days to start, especially if the cluster is busy or if you are requesting many GPUs.
    
- **Resource Allocation**: Uses idle resources on the cluster, so GPUs are not withdrawn from the account.
    
- **Job Duration**: Can run for up to four hours.
    

---

## Checking Job Status

You can check the status of your jobs using the `squeue` command. To see your jobs, use `squeue -u YOUR_USERNAME`. To get detailed information about a specific job, use `scontrol show job JOB_ID`.