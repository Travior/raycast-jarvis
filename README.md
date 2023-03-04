# raycast-jarvis
 
JARVIS stands for *Just A Rather Very Intelligent Server* and is a collection of server modules to interact with via web requests (for example with raycast extensions)

Each module is its own flask blueprint in the jarvis_modules module and is getting imported at runtime in the main.py file

Currently the list of modules consists of:
- sqldep: A tool that gives you all table dependencies of an SQL statement