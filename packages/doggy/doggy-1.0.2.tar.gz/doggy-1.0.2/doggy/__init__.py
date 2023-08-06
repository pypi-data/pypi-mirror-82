import click
import time
import random
from doggy.commands.uc import user_commands
from doggy.file_operations import create_profile,set_active_profile,get_current_profile,display_profiles,open_shortcut
import json

class active_user(object):
    def __init__(self,user_profile):
        self.user_profile = user_profile

@click.group(name="Basic_utilities",help="DOG͎̾GͧY͇",invoke_without_command=True)
@click.option("--actprof","-up",help="set the active user profile")
@click.option("--username","-un",help="use this in combination with --profilename/-pn to create a new profile")
@click.option("--profilename","-pn",help="use this in combination with the --username/-un option to create a new profile.")
@click.option("--shortcut","-sc",help="opens the specified shortcut for the user profile")
@click.pass_context
def main_commands(ctx,actprof,username,profilename,shortcut):
    ctx.obj = active_user(actprof)
    if(actprof != None):
        set_active_profile(actprof)
    if(username and profilename != None):
        create_profile(profilename,username)
    if(shortcut != None):
        open_shortcut(shortcut)
    pass
    

@main_commands.command(name="info",help="Provides basic info about the CLI application")
def info():
    time.sleep(1)
    click.secho("HEY THERE,",fg="red")
    time.sleep(2)
    click.secho("I am doggy your coding companion,",fg="magenta",bg="white")
    time.sleep(1.5)
    click.secho("You can make your coding life easier \b and simpler by making use of my powerful commands. LIKEEEEEE....",fg="magenta",bg="white")
    time.sleep(1.3)
    click.secho("----> You can create GITHUB repos or push changes to your GITHUB repo in just one command",fg="black",bg="magenta")
    time.sleep(1.5)
    click.secho("----> You can set shortcuts for all your workspaces as well as your code editors, so you dont have to go through all the clicking and searching for your folders.",fg="red",bg="white")
    time.sleep(1.5)
    click.secho("----> You can also make diff profiles based on your workflow and set passwords for each profile",fg="white",bg="red")
    time.sleep(2)
    click.secho("AND MUCH MUCH MORE, SO WHAT ARE YOU WAITING FOR GET CODING.....",fg="magenta")
    time.sleep(2)

@main_commands.command(name="currprof",help="Displays the current user profile chosen")
@click.pass_obj
def currprof(ctx):
    profile_name = get_current_profile()
    click.secho("The current profile is %s" % profile_name)

@main_commands.command(name="display",help="Displays all the user profiles")
def display():
    try:
        display_profiles()
    except:
        print("There are no user profiles available DUMBO, add some users and then ill display them.")

@main_commands.command(name="creator", help="opens the blog of the great creator of DOG͎̾GͧY͇")
def creator():
    click.launch("https://orangeappleak.github.io/")

main_commands.add_command(user_commands)