#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <dlfcn.h>
#include <dirent.h>
#include <string.h>
// Name: Dustin Shiao
// netID: ds1576
// RUID: 185004024
// your code for readdir goes here

struct dirent* readdir(DIR* dirp)
{
    struct dirent* dp;
    struct dirent* (*og_readdir)(DIR*);
    og_readdir = dlsym(RTLD_NEXT, "readdir");
    char* hide = getenv("HIDDEN");
    while((dp=og_readdir(dirp)))
    {
        if(strcmp(dp->d_name,hide)!=0)
            break;
    }
    return dp;
}