#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <dlfcn.h>
// Name: Dustin Shiao
// netID: ds1576
// RUID: 185004024
// your code for time() goes here

int first_time=0;

time_t time(time_t *tloc)
{
    time_t t;
    time_t (*og_time)(time_t*);
    og_time = dlsym(RTLD_NEXT,"time");
    if(first_time==0)
    {
        first_time++;
        t=1614725801;
    }
    else
        t = og_time(NULL);
    if(tloc)
        *tloc = t;
    return t;
}   