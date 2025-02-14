from attacker import ScriptLoader


a = ScriptLoader()
while True:
    command = input("> ")
    #try:
    if command == "exit":
        break
    elif command == "help":
        print("Help message")
    elif command == "execute":
        if a.payload == None or a.scripts == {}:
            print("No script loaded, loading scripts...")
            a.load_scripts()
            a.set_script()
        else:
            a.run_script(a.payload)
    elif command == "list":
        if a.scripts == {}:
            a.load_scripts()
        else:
            print("Scripts already loaded")
        a.view_scripts()
    #except Exception as e:
        #print(f"Error: {e}")
    