#include <stdio.h>
#include <sys/ptrace.h>
#include <sys/wait.h>
#include <unistd.h>
#include <sys/user.h>
#include <sys/syscall.h>
#include <sys/reg.h>
#include <stdlib.h>
#include <linux/kernel.h>
#include <linux/syscalls.h>

#define syscode_case(x) case x: return #x

const char* get_syscode(long);

struct user_regs_struct regs;

int main()
{
	pid_t child = fork();
	if(child == 0)
	{
		if(ptrace(PTRACE_TRACEME, 0, NULL, NULL) < 0)
		{
			perror("ptrace(PTRACE_TRACEME)");
			exit(1);
		}
		execl("/bin/ls", "ls", NULL);
	}
	else if(child < 0) printf("Fork failed.\n");
	else
	{
		int status;
		while(waitpid(child, &status, 0) && !WIFEXITED(status))
		{
			if(ptrace(PTRACE_GETREGS, child, NULL, &regs) < 0)
			{
				perror("ptrace(PTRACE_GETREGS)");
				exit(1);
			}
			fprintf(stderr, "[SYSCALL]:%-20s\t%5lld\n", get_syscode(regs.orig_rax), regs.orig_rax);
			if(ptrace(PTRACE_SYSCALL, child, NULL, NULL) < 0)
			{
				perror("ptrace(PETRACE_SYSCALL)");
				exit(1);
			}
		}
	}
	return 0;
}
