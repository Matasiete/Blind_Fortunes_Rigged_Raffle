# -*- coding: utf-8 -*-
"""
Created on Tue Jun  12 21:10

@author: Matasiete
Stable Version for options (all menu items)
"""

# Blind's Fortune Rigged Raffle

import datetime
import random
import ast             # Used in groups_per_num_players()
import os
import shutil          # Used to manage backups.

# ANSI Escape Codes for text coloring
COLOR_RESET = "\033[0m"         # For standard text
COLOR_GREEN = "\033[92m"        # User choices
COLOR_YELLOW = "\033[93m"       # Warnings or problems
COLOR_RED    = "\033[91m"       # User interaction required
COLOR_CYAN   = "\033[96m"       # Sessions, Groups or Players information outputs
COLOR_BOLD   = "\033[1m"        # REserved for future usage

# Declare Club name

ASSOCIATION_NAME = "-Board Gamers Club-"

"""
FUNCTION:
Acts as the primary execution framework and user interface controller 
for the program. It runs an infinite loop displaying a terminal menu 
that orchestrates session creation, users join, data visualization,
and data consistency and preserve until the user exits.

ARGUMENTS:
None.

RETURNS:
None (returns None implicitly upon termination).

DATA FLOW LINKS:
- Receives data from: None (invoked directly by the Python runtime execution guard).
- Delivers data to: Invokes and hands over control flow directly to group_management().
    """
def main():
        
    clear_terminal()

    # Call to presentation function. Presents current brefing
    display_welcome_screen()

    # Run file verification and backup engine at boot-up
    manage_backups_and_integrity()    


    # Declares empty variable for inputs
    answer = ""
    
    while answer != "5":
    
        clear_terminal()
        print ("==============================================")
        print (f"{COLOR_GREEN}    📋    MAIN MENU    📋     ")
        print ("==============================================\n")
        print ("     1. Create a new Session     ")
        print ("     2. List sessions/groups     ")
        print ("     3. Add a new player         ")
        print ("     4. List players             ")
        print ("     5. Exit program             ")
        print (f"{COLOR_RESET}")
        print ("==============================================\n")

        answer = input(f"{COLOR_RED}Select an option: (1-(5)) {COLOR_RESET}").strip()
        
        if answer == "1":
            clear_terminal()
            group_management()
        elif answer == "2":
            list_sessions_menu()
            clear_terminal()
        elif answer == "3":
            clear_terminal()
            add_new_player()
        elif answer == "4":
            clear_terminal()
            list_players_and_groups()
        # Count any other answer as a "5"
        else:
            answer == "5"
            print ("Finishing....")
            # This triggers the direct Step 4 rollback routine inside the function
            manage_backups_and_integrity(is_exit_control=True) 

    print (f"{COLOR_BOLD}Till next session. See ya'!")

# Minor function to simulate a screen cleanup
def clear_terminal():
    for i in range (40):
        print()

"""
FUNCTION: Validates structural database consistency for 'Players.txt' and 'Groups.txt'.
If valid, creates copies as 'old_Players.txt' and 'old_Groups.txt'.
If corrupted, attempts recovery from previous backups. For the very first use,
forces initialization of at least 2 players and 1 group before generating backups.
Offers a manual restore option before exiting to the main menu.

ARGUMENTS: None.

RETURNS: None.

DATA FLOW LINKS: - Receives data from: main() or group_management() upon session initialization.
                 - Delivers data to: Reads/Writes 'Players.txt', 'Groups.txt' and 'old_...' text files,
                   and clears the screen before returning control to main().
"""
def manage_backups_and_integrity(is_exit_control=False):

    # Declare file names    
    players_file = "Players.txt"
    groups_file = "Groups.txt"
    old_players = "old_Players.txt"
    old_groups = "old_Groups.txt"
    
    # Straight Jump: If an exit control is True goes to last step to recover/exit
    if is_exit_control:
        print(f"\n=============================================={COLOR_YELLOW}")
        print("🚪 EXIT CONTROL: Security Rollback Routine")
        print(f"{COLOR_RESET}==============================================\n\n")

        print("Confirm your session activities...")
        print(f"{COLOR_RED}🔄 Are you happy to SAVE today changes? ")
        print("Or do you want to RESTORE to yesterday's backup? ")

        restore_confirm = input(f"🔄 R/(S) to Restore or (SAVE default): {COLOR_RESET}").strip().upper()

        if restore_confirm == "R":

            if os.path.exists(old_players) and os.path.exists(old_groups):
                shutil.copy(old_players, players_file)
                shutil.copy(old_groups, groups_file)
                print(f"{COLOR_CYAN}✅ Success: Session changes discarded. Files rolled back to previous backup.{COLOR_RESET}")
                
            else:
                print(f"{COLOR_YELLOW}❌ Error: No backup files available to restore.{COLOR_RESET}")
        else:
            print(f"{COLOR_CYAN}▶️ Saving changes. Current session data successfully registered.{COLOR_RESET}")
            
            print("==============================================\n")
            input (f"{COLOR_RED}Enter to go on... {COLOR_RESET}")
            clear_terminal()
            
        return  # Cierra la función y permite que main() termine
    
    is_valid = True
    
    print(f"{COLOR_CYAN}\n==============================================")
    print("🛡️ DATABASE INTEGRITY & BACKUP MANAGEMENT")
    print("==============================================")
    print(f"Checking system files health...{COLOR_RESET}")
    print()
    print()

    # -------------------------------------------------------------------------
    # VERIFY INTEGRITY OF CURRENT DATABASES
    # -------------------------------------------------------------------------
    try:
        # Check Players list structure
        with open(players_file, "r", encoding="utf-8") as file:
            p_lines = file.read().splitlines()
            for line in p_lines:
                if line.strip() and (line.startswith("(") or line.startswith("[")):
                    # A player name line shouldn't look like a tuple or list structure
                    is_valid = False
                    break
                    
        # Check Groups structured collection layouts using AST
        with open(groups_file, "r", encoding="utf-8") as file:
            g_lines = file.read().splitlines()
            for line in g_lines:
                line = line.strip()
                if not line:
                    continue
                if "): " not in line:
                    is_valid = False
                    break
                key_part, value_part = line.split("): ", 1)
                key_part += ")"
                value_part = value_part.replace('true', 'True').replace('false', 'False')
                
                # If AST fails to parse strings back to tuple/list types, file is corrupted
                ast.literal_eval(key_part)
                ast.literal_eval(value_part)
    except (FileNotFoundError, ValueError, SyntaxError, IndexError):
        is_valid = False

    # -------------------------------------------------------------------------
    # HANDLE CORRUPTION / FIRST RUN INITIALIZATION
    # -------------------------------------------------------------------------
    ## Management of not valid current files
    if not is_valid:
        print(f"{COLOR_YELLOW}⚠️ Warning: System detected a missing or malformed database layout.")
        
        # Check if backup files exist to recover from them
        if os.path.exists(old_players) and os.path.exists(old_groups):
            print("🔄 Valid previous backups found! Recovering state data...")
            # Recovery from backup
            shutil.copy(old_players, players_file)
            shutil.copy(old_groups, groups_file)
            print(f"✅ Restoration complete. System files recovered successfully.{COLOR_RESET}")
        else:
            # FIRST RUN SCENARIO: No files or backups exist. Files need to be created
            print("\n📥 [FIRST RUN DETECTED] Initializing system from scratch...")
            print(f"You must register a starting group with AT LEAST 2 new players.{COLOR_RESET}")
            
            initial_players = []
            player_count = 1
            
            # Force user to input at least 2 distinct unique player names
            while len(initial_players) < 2:
                name_input = input(f"{COLOR_RED}Enter unique name for Player #{player_count}: ").strip()
                if not name_input:
                    print("❌ Name cannot be empty.")
                    continue
                if name_input in initial_players:
                    print("❌ Rejection: Player names must be unique.")
                    continue
                initial_players.append(name_input)
                player_count += 1
            print()
            print(f"{COLOR_RESET}")

            # Save the players to the master file
            with open(players_file, "w", encoding="utf-8") as file:
                for player in initial_players:
                    file.write(player + "\n")
            
            # Formulate the first group G1 structure automatically
            today = datetime.datetime.now()
            today_str = f"{today.year}-{today.month}-{today.day}"
            total_n = len(initial_players)
            
            # Player 0 becomes the initial leader by default for initialization setup
            with open(groups_file, "w", encoding="utf-8") as file:
                for idx, player in enumerate(initial_players):
                    is_leader = "True" if idx == 0 else "False"
                    game_date = f'"{today_str}"' if idx == 0 else '""'
                    record_line = f'("G1",{total_n},"{player}"): [{is_leader},{idx},{game_date}]\n'
                    file.write(record_line)
            
            # Generate the first baseline backups immediately
            shutil.copy(players_file, old_players)
            shutil.copy(groups_file, old_groups)
            print(f"{COLOR_CYAN}✨ Initial databases and backups created successfully under group 'G1'.")
            
            print(f"==============================================\n{COLOR_RED}")
            print()
            print()
            input (f"Enter to go on... {COLOR_RESET}")
            clear_terminal()
            return


    else:   
        # -------------------------------------------------------------------------
        # OFFER MANUAL RECOVERY BEFORE EXITING ROUTINE
        # -------------------------------------------------------------------------
        print(f"{COLOR_CYAN}=============================================={COLOR_RESET}\n")
        restore_confirm = input(f"{COLOR_RED}🔄 Do you want to RESTORE yesterday's backup profiles instead? y/(N): {COLOR_RESET}").strip().lower()
        if restore_confirm == "y":
            if os.path.exists(old_players) and os.path.exists(old_groups):
                shutil.copy(old_players, players_file)
                shutil.copy(old_groups, groups_file)
                print(f"{COLOR_BOLD}✅ Success: Live files replaced with previous backup data state.{COLOR_RESET}")
            else:
                print(f"{COLOR_YELLOW}❌ Error: No backup files available to complete the action.{COLOR_RESET}")
        else:
            print(f"{COLOR_CYAN}▶️ Keeping current live data files intact.")
            
        print(f"=============================================={COLOR_RED}")
        print()
        print()

        # -------------------------------------------------------------------------
        # CREATE NEW BACKUPS FROM VALID LIVE DATABASES
        # ------------------------------------------------------------------------- 
        print(f"{COLOR_CYAN}✅ Integrity verified. Creating new backup files")
        shutil.copy(players_file, old_players)
        shutil.copy(groups_file, old_groups)
        print(f"📝 Backups overwritten and updated successfully.{COLOR_RED}")
        print()
        print()

        input(f"{COLOR_RED}\n[Press 'ENTER' to clear this dashboard and open the Main Menu]: {COLOR_RESET}")
        clear_terminal()
        
    
""" display_welcome_screen()
FUNCTION: Displays a structured welcome dashboard showcasing live database statistics 
for the registered association, including total players, unique historical 
groups, and session counts classified by group sizes. Prompts for an input 
before transitioning to the main menu.

ARGUMENTS: None.

RETURNS: None.

DATA FLOW LINKS: - Receives data from: main() at the very start of program execution.
                 - Delivers data to: Invokes clear_terminal() upon user confirmation to 
                   give way to the main loop menu layout.
"""    
def display_welcome_screen():
    players_file = "Players.txt"
    groups_file = "Groups.txt"
    
    total_players = 0
    unique_groups_set = set()
    
    # Dictionary to keep track of unique Gxxx codes per size
    # Data Type: dict -> Key: int (Size N) -> Value: set of strings (Unique Gxxx codes)
    groups_by_size_tracker = {}

    # 1. Gather stats from Players.txt
    try:
        with open(players_file, "r", encoding="utf-8") as file:
            player_set = set(file.read().splitlines())
            total_players = len([p for p in player_set if p.strip()])
    except FileNotFoundError:
        total_players = 0

    # 2. Gather stats from Groups.txt
    try:
        with open(groups_file, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line or "): " not in line:
                    continue
                
                key_part, _ = line.split("): ", 1)
                key_part = key_part + ")"
                
                # Safely convert the left side to an actual Python tuple
                key_tuple = ast.literal_eval(key_part)
                
                g_code = key_tuple[0]       # Extracts "Gxxx" string (e.g., "G1")
                group_size = key_tuple[1]   # Extracts the integer size (e.g., 3)
                
                # Global unique group counter tracking
                unique_groups_set.add(g_code)
                
                # Track unique group configurations by their player count size
                # If "G4" is read multiple times, the set ensures it is only counted once
                if group_size not in groups_by_size_tracker:
                    groups_by_size_tracker[group_size] = set()
                groups_by_size_tracker[group_size].add(g_code)
    except FileNotFoundError:
        pass

    total_groups = len(unique_groups_set)

    # 3. Render Dashboard Interface Visual Output
    clear_terminal()
    print("=====================================================")
    print(f"{COLOR_CYAN}🌟 WELCOME TO THE {ASSOCIATION_NAME.upper()} 🌟")
    print("=====================================================")
    print("📊 CURRENT SYSTEM STATISTICS:")
    print("-----------------------------------------------------")
    print(f"👤 Total Registered Players : {total_players}")
    print(f"🎲 Total Unique Game Groups : {total_groups}")
    print("-----------------------------------------------------")
    print("📦 Registered Groups Classified by Size:")
    
    if groups_by_size_tracker:
        # Sort keys to display sizes chronologically (Blocks of 3, Blocks of 4...)
        for size in sorted(groups_by_size_tracker.keys()):
            # The real group count is the length of the set containing unique Gxxx strings
            real_group_count = len(groups_by_size_tracker[size])
            print(f"   🔹 Groups with {size} Players: {real_group_count} unique configurations")
    else:
        print(f"   🔹 No game groups registered in the database yet.{COLOR_RESET}")
        
    print(f"{COLOR_RESET}=====================================================\n")
    
    
    # 4. Trigger blocking input screen clear prompt to move forward
    input(f"{COLOR_RED}\n[Press 'ENTER' to clear this dashboard and go to Data Check]: {COLOR_RESET}")
    clear_terminal()
    
    
    
"""
FUNCTION: Prompts the user for a new player name, reads 'Players.txt' into a set 
data type to guarantee unique string entries, and appends the new player 
only if the name does not already exist in the database.

ARGUMENTS: None.

RETURNS: None.

DATA FLOW LINKS: - Receives data from: main() when the user enters option "p".
                 - Delivers data to: Appends a unique new row entry directly into 'Players.txt'.
"""
def add_new_player():

    filename = "Players.txt"
    
    print(f"{COLOR_GREEN}\n==============================================")
    print("👤 ADD A NEW PLAYER TO REGISTRY")
    print(f"=============================================={COLOR_RED}")
    
    new_name = input(f"Enter the new player name: {COLOR_RESET}").strip()
    
    # Reject empty inputs immediately
    if new_name == "":
        print(f"{COLOR_YELLOW}❌ Error: Player name cannot be empty.{COLOR_RESET}")
        return

    # Read existing file into a SET to guarantee absolute uniqueness
    # existing_players Data Type: set of strings -> {"P1", "P2", "P3"}
    try:
        with open(filename, "r", encoding="utf-8") as file:
            # splitlines() removes hidden '\n' characters cleanly
            existing_players = set(file.read().splitlines())
    except FileNotFoundError:
        # If the file doesn't exist yet, initialize an empty set legitimately
        existing_players = set()

    # Check existence and handle rejection or insertion
    if new_name in existing_players:
        print(f"{COLOR_YELLOW}❌ Rejection: The player '{new_name}' already exists in the registry.{COLOR_RESET}")
    else:
        # Confirm insertion with the user
        confirm = input(f"{COLOR_RED}Are you sure you want to register '{new_name}'? y/(N): {COLOR_RESET}").strip().lower()
        if confirm == "y":
            # 3. Append safely using "a" mode
            with open(filename, "a", encoding="utf-8") as file:
                file.write(new_name + "\n")
            print(f"{COLOR_CYAN}✅ Success: '{new_name}' has been added to {filename}.{COLOR_RESET}")
        else:
            print(f"{COLOR_YELLOW}❌ Operation aborted by the user.{COLOR_RESET}")
               
    print("==============================================\n")
    input (f"{COLOR_RED}Enter to go on... {COLOR_RESET}")
    clear_terminal()
    

"""
FUNCTION: Displays a secondary sub-menu to query historical game data from 'Groups.txt'.
Allows filtering blocks either by group size (showing the upcoming leader), 
by a specific player's name (grouped by session size), or by a specific 
group code name (showing its full roster and next rotative leader).

ARGUMENTS: None.

RETURNS: None.

DATA FLOW LINKS: - Receives data from: main() when the user enters option "s".
                 - Delivers data to: Invokes groups_per_num_players() for option 1, 
                   reads 'Groups.txt' directly for options 2 and 3, and prints terminal logs.
"""
def list_sessions_menu():

    filename = "Groups.txt"
    
    print("\n=================================================================")
    print(f"{COLOR_GREEN}📊 SESSION LISTING SUB-MENU")
    print("=================================================================")
    print("1. Filter by Number of Players (Show next leader)")
    print("2. Filter by Player Name (Grouped by group size)")
    print("3. Filter by a Particular Group Name (Show members & next leader)")
    print(f"4. Return to Main Menu{COLOR_RESET}")
    print("=================================================================\n")
    
    sub_answer = input(f"{COLOR_RED}Select an option (1-4): ").strip()
    
    # -------------------------------------------------------------------------
    # OPTION 1: FILTER BY NUMBER OF PLAYERS
    # -------------------------------------------------------------------------
    if sub_answer == "1":
        try:
            size_input = int(input("\nEnter group size to filter (N): "))
        except ValueError:
            print(f"{COLOR_YELLOW}❌ Invalid number. Returning to main menu.{COLOR_RESET}")
            return
            
        groups_dict = groups_per_num_players(size_input)
        if not groups_dict:
            return
            
        g_map = {}
        for key_tuple, value_list in groups_dict.items():
            g_code = key_tuple[0]
            if g_code not in g_map:
                g_map[g_code] = []
            g_map[g_code].append((key_tuple[2], value_list[0], value_list[1], value_list[2]))
            
        print(f"{COLOR_CYAN}\n📋 SESSIONS RECORD FOR {size_input} PLAYERS: ")
        print("----------------------------------------------")
        for g_code, players_data in sorted(g_map.items()):
            players_data.sort(key=lambda item: item[2])
            current_leader_name = "Unknown"
            current_leader_order = -1
            total_n = len(players_data)
            
            player_names_list = []
            for name, is_leader, order, date_str in players_data:
                player_names_list.append(name)
                if is_leader:
                    current_leader_name = name
                    current_leader_order = order
            
            next_order_idx = (current_leader_order + 1) % total_n
            next_leader_name = "Unknown"
            for name, _, order, _ in players_data:
                if order == next_order_idx:
                    next_leader_name = name
                    break
                    
            print(f"🔹 Group: {g_code} | Roster: {player_names_list}")
            print(f"   Current Session Leader: {current_leader_name}")
            print(f"   🚀 Upcoming Rotative Leader next time: {next_leader_name}")
            print("----------------------------------------------")

    # -------------------------------------------------------------------------
    # OPTION 2: FILTER BY PLAYER NAME
    # -------------------------------------------------------------------------
    elif sub_answer == "2":
        target_player = input("\nEnter player name to search (e.g., P1): ").strip()
        size_map = {}
        
        try:
            with open(filename, "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if not line or "): " not in line:
                        continue
                        
                    key_part, value_part = line.split("): ", 1)
                    key_part = key_part + ")"
                    value_part = value_part.replace('true', 'True').replace('false', 'False')
                    key_tuple = ast.literal_eval(key_part)
                    
                    g_code = key_tuple[0]
                    group_size = key_tuple[1]
                    player_name = key_tuple[2]
                    
                    if player_name == target_player:
                        if group_size not in size_map:
                            size_map[group_size] = []
                        if g_code not in size_map[group_size]:
                            size_map[group_size].append(g_code)
        except FileNotFoundError:
            print(f"{COLOR_YELLOW}❌ Error: '{filename}' file not found.{COLOR_RESET}")
            return
            
        if not size_map:
            print(f"{COLOR_YELLOW}❌ No historical records found for player '{target_player}'.{COLOR_RESET}")
            return
            
        print(f"{COLOR_CYAN}\n📋 HISTORICAL SESSIONS FOR PLAYER: '{target_player}'")
        print("==============================================")
        for size in sorted(size_map.keys()):
            groups_list = sorted(size_map[size])
            print(f"📦 Blocks of {size} Players:")
            print(f"   Joined Groups: {groups_list}")
            print("----------------------------------------------")

    # -------------------------------------------------------------------------
    # OPTION 3: FILTER BY A PARTICULAR GROUP NAME (Show members & next leader)
    # -------------------------------------------------------------------------
    elif sub_answer == "3":
        target_group = input("\nEnter Group Name to search (e.g., G1): ").strip().upper()
        
        # Structure to collect matching entries
        # matching_players Data Type: list of tuples -> [(name, is_leader, order, date_str)]
        matching_players = []
        group_size_found = 0
        
        try:
            with open(filename, "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if not line or "): " not in line:
                        continue
                        
                    key_part, value_part = line.split("): ", 1)
                    key_part = key_part + ")"
                    value_part = value_part.replace('true', 'True').replace('false', 'False')
                    key_tuple = ast.literal_eval(key_part)
                    value_list = ast.literal_eval(value_part)
                    
                    g_code = key_tuple[0]
                    
                    # If this line matches the searched Gxxx code, extract details
                    if g_code == target_group:
                        group_size_found = key_tuple[1]
                        player_name = key_tuple[2]
                        is_leader = value_list[0]
                        player_order = value_list[1]
                        last_date = value_list[2]
                        
                        matching_players.append((player_name, is_leader, player_order, last_date))
        except FileNotFoundError:
            print(f"{COLOR_YELLOW}❌ Error: '{filename}' file not found.{COLOR_RESET}")
            return

        if not matching_players:
            print(f"{COLOR_YELLOW}❌ Group '{target_group}' does not exist in the records.{COLOR_RESET}")
            return
            
        # Sort players by their internal game choice priority order (Turn 0, 1, 2...)
        matching_players.sort(key=lambda item: item[2])
        total_n = len(matching_players)
        
        # Track leadership status to calculate the next cyclic index
        current_leader_name = "Unknown"
        current_leader_order = -1
        player_names_list = []
        
        # Get current leader Name and order value
        for name, is_leader, order, _ in matching_players:
            player_names_list.append(name)
            if is_leader:
                current_leader_name = name
                current_leader_order = order
                
        # Calculate upcoming leader rotation index safely using modulo
        next_order_idx = (current_leader_order + 1) % total_n
        next_leader_name = "Unknown"
        for name, _, order, _ in matching_players:
            if order == next_order_idx:
                next_leader_name = name
                break
        
        # Present details homogeneously
        print(f"{COLOR_CYAN}\n📋 DETAILS FOR GROUP: '{target_group}'")
        print("==============================================")
        print(f"🔹 Total Members (N): {group_size_found}")
        print(f"🔹 Group Roster: {player_names_list}")
        print("----------------------------------------------")
        
        for name, is_leader, order, date_str in matching_players:
            role_label = "👑 CURRENT LEADER" if is_leader else "   follower"
            date_display = f" [Active since: {date_str}]" if (is_leader and date_str) else ""
            print(f"   Turn Order {order}: {name:<10} | {role_label}{date_display}")
            
        print("----------------------------------------------")
        print(f"🚀 Upcoming Rotative Leader next time: {next_leader_name}")
        print(f"==============================================\n{COLOR_RESET}")

    elif sub_answer == "4":
        print("Returning to main menu...")
    else:
        print("❌ Invalid choice option.")

    print("==============================================\n")
    input (f"{COLOR_RED}Enter to go on... {COLOR_RESET}")
    clear_terminal()


"""
FUNCTION:
Reads the master 'Players.txt' file and cross-references it with 'Groups.txt'
to display a read-only clean list of all registered players and the specific
historical groups ('Gxxx') they belong to.

ARGUMENTS:
None.

RETURNS:
None.

DATA FLOW LINKS:
- Receives data from: main() when the user enters option "l".
- Delivers data to: Only outputs visual logs to the terminal interface.
"""
def list_players_and_groups():

    players_file = "Players.txt"
    groups_file = "Groups.txt"
    
    # 1. Read master registered players list
    try:
        with open(players_file, "r", encoding="utf-8") as file:
            all_players = file.read().splitlines()
        # Clean any trailing whitespaces or empty elements
        all_players = [p.strip() for p in all_players if p.strip()]
    except FileNotFoundError:
        print(f"\n❌ Error: '{players_file}' database file not found. Add players first.")
        return

    if not all_players:
        print("\n📝 Master players database is empty.")
        return

    # 2. Parse Groups.txt to map players to their respective groups
    # Structure -> player_maps = {"P1": {"G1", "G2"}, "P2": {"G1"}}
    player_maps = {player: set() for player in all_players}
    
    try:
        with open(groups_file, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line or "): " not in line:
                    continue
                
                # Split key part to parse the tuple
                key_part, _ = line.split("): ", 1)
                key_part = key_part + ")"
                
                # Safely convert left side to actual Python tuple
                key_tuple = ast.literal_eval(key_part)
                
                group_code = key_tuple[0]   # Extracts "Gxxx"
                player_name = key_tuple[2]  # Extracts "Pxx"
                
                # If the player is in our master list registry, track the group code
                if player_name in player_maps:
                    player_maps[player_name].add(group_code)

    except FileNotFoundError:
        # If Groups.txt doesn't exist yet, we can still list players with empty groups
        pass

    # 3. Homogeneous visual print terminal output
    print("\n========================================================")
    print(f"{COLOR_CYAN}📋 REGISTERED PLAYERS & HISTORICAL GROUPS")
    print("========================================================")
    
    for player in sorted(all_players):
        # Sort group codes alphabetically for a cleaner interface look
        associated_groups = sorted(list(player_maps[player]))
        
        if associated_groups:
            # Join list into a clean comma separated string format -> G1, G2, G4
            groups_str = ", ".join(associated_groups)
        else:
            groups_str = "None (No sessions registered yet)"
            
        print(f"👤 Player: {player:<10} | Member of: [{groups_str}]")
        
    print(f"======================================================\n{COLOR_RESET}")

    input (f"{COLOR_RED}ENTER to go back to Main Menu {COLOR_RESET}")
    clear_terminal()

""" list_randomizer(session_members)
FUNCTION: Shuffles the players list multiple times (2-6 rounds) to randomize turn 
priority and determine a session leader.

ARGUMENTS: - session_members (list): Current list of player names attending the game.

RETURNS: - session_members (list): The newly reordered list where index [0] is the leader.

DATA FLOW LINKS:
- Receives data from: group_creation(session_members)
- Delivers data to: Returns the shuffled list back to group_creation(session_members).
""" 
def list_randomizer (session_members):
    
    print(f"{COLOR_CYAN}--------------------------------")
    # List (indexed and so random pickable)
    session_members = list(session_members)
    #number of lottery drum turns
    rand_iterations = int(random.randint (2,6))
    
    for x in range (rand_iterations):
    
        selection = []
        print (f"{COLOR_GREEN}This is {x}'th' drum turn.......{COLOR_CYAN}")
        for y in range (len(session_members)):
            members_num = len(session_members)  
            rand_pick = int(random.randint(0, members_num -1))
            selected = session_members.pop(rand_pick)
            selection.append(selected)
            print (selection)
            
        session_members = selection
    print(f"{COLOR_CYAN}--------------------------------")
    print (f"And the leader is: {session_members[0]}")
    print(f"--------------------------------{COLOR_RESET}")
    #session_members = set(session_members)
    return session_members
    

""" group_creation(session_members)
FUNCTION: Creates a new group code (Gxxx+1), prompts for user confirmation, and appends 
the randomized player records, roles, and dates into 'Groups.txt'. 1 Player sessions not allowed

ARGUMENTS: - session_members (list): Current list of player names attending the game.

RETURNS:- new_group (str): The newly generated group identifier code (e.g., "G3").
        - False (bool): If the creation process is aborted by the user.

DATA FLOW LINKS: - Receives data from: group_management() or manage_new_session(session_members).
                 - Delivers data to: Passes session_members to list_randomizer(session_members) and 
                  returns the group code/False back to the caller function.
"""     
def group_creation(session_members):
    print("This is a new Player's Group!")
    
    if len(session_members) < 2:
        print("\n❌ Error: But cannot create a group. A minimum of 2 players is required.")
        print("This software is designed for multiplayer session management.")
        input("\n[Press 'ENTER' to return to the Main Menu]: ")
        return False  # Exits early returning False to indicate abortion
    
    print("Let's create the rotative Session Leader list...")
    
    # Run the lottery drum to shuffle players
    session_members = list_randomizer(session_members)
    
    
    # Ask for confirmation HERE, before opening/modifying any files
    print(f"\nProposed order: {session_members}")
    confirm = input("Ok to create a new group with this order? y/(N): ").strip().lower()
    if confirm != "y":
        print("Operation aborted. No records were written.")
        return False  # Exit early if user declines
    
    with open("Groups.txt", "r", encoding="utf-8") as file:
        lines = file.read().splitlines()
    
        # If there's data, get last line; if empty, create from scratch with G1
        if lines:
            last_line = lines[-1]
        else:
            ## Pending creation from Scratch
            last_line = '("G0",0,"")' #Dummy for previuos record
            print()
        
        
        # Spliting by '"' will divide line in parts.
        # Line example: '("G2", 4,"P4"): ...'
        # Will result in this parts: ('', 'G2', ', 4,', 'P4', '): ...']
        parts = last_line.split('"')
        last_group = parts[1]  # i.e. "G2"
        
        # Remove letter 'G' and convert the rest to int
        last_num = int(last_group.replace("G", ""))
        
        # Get the following number
        new_num = last_num + 1
        new_group = f"G{new_num}"  # i.e. "G3"
       
    # Read raw date for the game day
    current_date = datetime.datetime.now()
    # Format the game date
    current_date = f'{current_date.year}-{current_date.month}-{current_date.day}'
    # Count players for the game
    members_number = len(session_members)
    
    # Present the group details creation
    print (f"Creating new {new_group} group for {current_date} session...")
    # Open groups records file to write new group details.
    
    # Open and write everything safely in one single clean block
    with open("Groups.txt", "a", encoding="utf-8") as file:
        for x in range(members_number):
            leader = True if x == 0 else False
            game_date = f'"{current_date}"' if x == 0 else '""'
            
            record_line = f'("{new_group}",{members_number},"{session_members[x]}"): [{leader},{x},{game_date}]\n'
            role = "leader" if leader else "follower"
            print(f'Adding {session_members[x]} as {role} and "{x}"th group player.')
            
            file.write(record_line) 
    
    
    # Returns ne group name or False as a group created or not control
    return new_group #result 
        

""" group_management()
FUNCTION: Coordinates player input verification and routes the session flow by determining 
if the player combination is completely new or already exists in the history database.

ARGUMENTS: None.

RETURNS: None (returns None implicitly upon termination).

DATA FLOW LINKS: 
- Receives data from: main().
- Delivers data to: Passes 'session_members' to manage_session_members(), 
  'members_num' to groups_per_num_players(), and routes flow to group_creation() 
  or check_group_existence().
"""
def group_management():
    
    session_members = []
    
    # Call manage_session_members funtion
    # Two values are returned from  manage session_members with current session members as argument
    # Those are the names list of the members and a boolean for a possible new group.
    session_members , new_group = manage_session_members (session_members)
    
    members_num = len(session_members)
    ## If new_group is True is because there was a new player
    ## But what-if the combination of players itserf is the new factor?
    
 
    # CASE 1: A brand new player was registered during the inputs setup (new_group is True)
    # This automatically forces the creation of a brand new history group layout
    if new_group:
        print(f"{COLOR_YELLOW}\n🆕 New player detected! Forcing new group creation...")
        creation_result = group_creation(session_members)

        print(f"{COLOR_YELLOW}")
        if creation_result:
            print(f"✅ {creation_result} created successfully.")
        else:
            print("❌ Group creation was aborted.")    
        print(f"{COLOR_RESET}")

        
    # CASE 2: All players already existed in the database (new_group is False)
    # We must check whether this specific combination of names has met before
    else:
        # Fetch all historical records matching this specific group size
        # Standardized spelling variable name using single 'p'
        filtered_groups_dict = groups_per_num_players(members_num)
        
        print(f"{COLOR_YELLOW}")
        # If no historical records exist with this database entry count, it is a new combination
        if not filtered_groups_dict:
            print("\n📢 No historical groups match this size. Creating new session...")
            creation_result = group_creation(session_members)
        else:
            # Call your Topic 4 function to look for a matching name combination layout
            combo_exists, matching_g_code = check_group_existence(filtered_groups_dict, session_members)
            
            if combo_exists:
                print(f"🎯 Matching Group found for those players {matching_g_code}!. Launching routine...")
            
                # Call the rotation engine routine
                manage_existing_session(filtered_groups_dict, matching_g_code, session_members)
    
            else:
                # Groups of this size exist, but none contains this exact combination of player names
                print("\n📢 Known players but this specific combination layout is completely new!")
                creation_result = group_creation(session_members)

    print("------------------------------")
    print(f"The {members_num} members for this session are: {session_members}")
    print("------------------------------")
    print(f"{COLOR_RESET}")

"""
FUNCTION: Rotates the leadership to the next consecutive player for an existing group 
using cyclic modulo arithmetic, updates the session date string for the new 
leader, and performs a full database rewrite to persist updates in 'Groups.txt'.

ARGUMENTS: - filtered_groups_dict (dict): Keys = tuple ("Gxxx", N, "Pxx") | Values = list [bool, int, str].
           - group_code (str): The specific matching 'Gxxx' group identifier code (e.g., "G1").
           - session_members (list): Current list of player names attending tonight's session.

RETURNS: - group_code (str): The active 'Gxxx' identifier code processed by the routine.

DATA FLOW LINKS: - Receives data from: group_management().
                 - Delivers data to: Returns the active group code string back to group_management() 
                  after executing terminal tracking logs and modifying 'Groups.txt'.
"""
def manage_existing_session(filtered_groups_dict, group_code, session_members):

    # 1. Isolate entries only belonging to this specific Gxxx group code
    # group_data Structure -> { "P1": [False, 0, "date"], "P2": [True, 1, ""] }
    group_data = {}
    for key, value in filtered_groups_dict.items():
        if key[0] == group_code:
            player_name = key[2]
            group_data[player_name] = value

    total_players = len(group_data)
    
    # 2. Find who is the current leader and their rotation order index
    current_leader = ""
    current_order = -1
    
    for player, status in group_data.items():
        if status[0] is True:  # Found the active leader
            current_leader = player
            current_order = status[1]
            break

    # 3. Calculate the NEXT leader using cyclic modulo arithmetic
    next_order = (current_order + 1) % total_players
    next_leader = ""
    
    for player, status in group_data.items():
        if status[1] == next_order:
            next_leader = player
            break

    print(f"\n🔄 Existing group {group_code} detected.")
    print(f"Previous session leader was: {current_leader} (Order {current_order})")
    print(f"👑 New rotated leader for tonight is: {next_leader} (Order {next_order})")

    # 4. Get today's formatted date string
    today = datetime.datetime.now()
    today_str = f"{today.year}-{today.month}-{today.day}"

    # 5. Read the ENTIRE Groups.txt file to prepare a full rewrite update
    with open("Groups.txt", "r", encoding="utf-8") as file:
        all_lines = file.read().splitlines()

    updated_lines = []
    for line in all_lines:
        line = line.strip()
        if not line or "): " not in line:
            updated_lines.append(line + "\n")
            continue

        # Extract keys to identify if this line belongs to our target group
        key_part, value_part = line.split("): ")
        key_part = key_part + ")"
        key_tuple = ast.literal_eval(key_part)
        value_list = ast.literal_eval(value_part) 

        # If the line matches our active Group Code, modify its content values
        if key_tuple[0] == group_code:
            current_player = key_tuple[2]
            player_order = value_list[1]    # Keeps the same order index from the file
            
            # We get the date that the player already had in the file
            # value_list[2] is saved date (i.e.: "2026-6-10" or "")
            historical_date = value_list[2]
            
            # Check if the player is the session new leader
            is_new_leader = (current_player == next_leader)
            is_leader_bool = True if is_new_leader else False
            
            # Dates rule
            # If new leader, register current date.
            # Anyother one keeps his date record.
            game_date = f'"{today_str}"' if is_new_leader else f'"{historical_date}"'
            
            # Reconstruct the homogeneous format row string entry
            new_record = f'("{group_code}",{total_players},"{current_player}"): [{is_leader_bool},{player_order},{game_date}]'
            #new_record = f'("{group_code}",{total_players},"{current_player}"): [{is_leader_str},{player_order},{game_date}]'
            updated_lines.append(new_record + "\n")
            
            # Print homogeneous output terminal tracking feedback logs
            role_label = "leader" if is_new_leader else "follower"
            print(f'Updating {current_player} as {role_label} and "{player_order}"th group player.')
        else:
            # Leave other groups completely untouched
            updated_lines.append(line + "\n")

    # 6. Write the entire modified content database stack back to Groups.txt
    with open("Groups.txt", "w", encoding="utf-8") as file:
        file.writelines(updated_lines)

    print(f"📝 Database updated successfully for existing group {group_code}.\n")
    return group_code

""" check_group_existence(resultado: dict, session_members: list)
FUNCTION: Checks if there is any historical group code ('Gxxx') in the filtered database 
records where all current session players are present at the same time.

ARGUMENTS: - resultado (dict): Filtered history records mapping tuples to list parameters.
           - session_members (list): Current list of player names attending the session.

RETURNS: - tuple (bool, str/None): Returns (True, "Gxxx") if an exact combination match 
  is found, or (False, None) if the combination layout is completely new.

DATA FLOW LINKS: - Receives data from: group_management().
                 - Delivers data to: Returns the verification boolean state flag and the group code 
                 back to group_management().
 """
def check_group_existence(resultado: dict, session_members: list):

    # Convert current players to a set to allow order-independent comparison
    # Data Type: set of strings
    current_players_set = set(session_members)
    
    # Extract all unique 'Gxxx' group codes present in your filtered results
    # Data Type: set of strings -> {'G1', 'G2'}
    unique_g_codes = {clave[0] for clave in resultado.keys()}
    
    # Iterate through each unique group code found in the history
    # group_code Data Type: str
    for group_code in unique_g_codes:
        
        # Extract all players belonging to the current 'group_code' loop iteration
        # Data Type: set of strings
        historical_players_set = {clave[2] for clave in resultado.keys() if clave[0] == group_code}
        
        # If the historical group set matches your current session set exactly:
        if historical_players_set == current_players_set:
            print(f"🎯 YES! Group '{group_code}' contains all N named players.")
            return True, group_code
            
    print("❌ NO! There is no group where all N named players are present together.")
    return False, None


""" groups_per_num_players(filter_value)
FUNCTION: Reads 'Groups.txt' line by line and converts raw string lines into structured data, 
filtering and collecting only the entries that match the specified group size.

ARGUMENTS: - filter_value (int): The current session group size (total number of players).

RETURNS: - result (dict): A dictionary containing all historical entries for that specific 
  group size, mapping tuple keys to their status list parameters.

DATA FLOW LINKS: - Receives data from: group_management().
                 - Delivers data to: Returns the filtered dictionary back to group_management() to 
                  be evaluated for group existence.
"""
def groups_per_num_players(filter_value):

    result = {}
    
    # 1. Line by line read fie
    with open("Groups.txt", "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:  # Skip empty lines if any
                continue
            # Correction: If no '): ' present, ignore and skip
            elif  "): " not in line:
                continue
                
            # Each line with the structure -> "Key": "value"
            # Divide left part (key) from right part (value) per characters '): '
            key_part, value_part = line.split('): ')
            
            # Rebuild lost parentesis on split by  '): '
            key_part = key_part + ')'
            
            
            # 2. Convert text in Python data types (Lists) using module ast.
            key_list = ast.literal_eval(key_part)
            value_list = ast.literal_eval(value_part)
            
            # 3. Converts key_list to a tuple data type  (lists cannot be dictionary keys)
            tuple_key = tuple(key_list)
            
            # 4. USe dinamic filtering on the fly at read-time
            if tuple_key[1] == filter_value:
                result[tuple_key] = value_list
    

    if not result:
        print ("No such a group registered")
        input (f"{COLOR_YELLOW}Enter to go on... {COLOR_RESET}")
        clear_terminal()
        
    return result


""" manage_new_session(session_members)
FUNCTION: Manages the creation and registration of a brand new session group when all 
attending players already exist individually but have never met in this specific 
combination before. 1 Player sessions not allowed

ARGUMENTS: - session_members (list): Current list of player names attending the session.

RETURNS: - tuple (list, str/bool): Returns the randomized session members list along with 
  the new group code identifier (or False if the process was aborted).

DATA FLOW LINKS: - Receives data from: group_management().
                 - Delivers data to: Passes 'session_members' forward to group_creation() and 
                  returns the updated tracking parameters back to group_management().
"""
def manage_new_session(session_members):

    if len(session_members) < 2:
        print("\n❌ Error: Cannot manage a new session. A minimum of 2 players is required.")
        print("Solitaire sessions do not require my Raffle Rotation tracking.")
        input("\n[Press 'ENTER' to return to the Main Menu]: ")
        return session_members, False  # Returns clean defaults to prevent main framework unpack crash
    
    print ("===================================================")
    print(f"\n{COLOR_CYAN}--------------------------------------------------")
    print(" NOTICE: This specific combination of players has NEVER met before!")
    print("A brand new group needs to be registered in the system.")
    print(f"--------------------------------------------------\n{COLOR_RESET}")
    print ("===================================================")
    
    # Uses group_creation to find the next Gxxx (+1), handle inputs,
    # run the lottery drum, and append records to Groups.txt
    # Data Type returned: str (e.g., "G3") or bool (False if aborted)
    new_group_code = group_creation(session_members)
    
    if new_group_code:
        print(f"\n✅ Successfully registered new group combination as: {new_group_code}")
        # Since group_creation internally calls list_randomizer, we need to pass 
        # the finalized order back to the main flow.
        # However, because group_creation doesn't return the list, we fetch it here.
        # Alternatively, we make sure it returns a control flag.
        new_group = new_group_code
    else:
        print("\n❌ Group creation was aborted by the user or failed.")
        new_group = False

    # Return both values to avoid the "unpack non-iterable" crash
    # session_members Data Type: list
    # new_group Data Type: str or bool
    return session_members, new_group
    
        
""" manage_session_members(session_members)
FUNCTION: Prompts user interface inputs to build the current session roster, verifies if 
any player is new to append them to 'Players.txt', and triggers a new group flag.

ARGUMENTS: - session_members (list): An empty list placeholder passed from the caller.

RETURNS: - session_members (list): The finalized list of player names attending tonight.
         - new_group (bool): True if a brand new player was appended to the master registry.

DATA FLOW LINKS: - Receives data from: group_management().
                 - Delivers data to: Returns both the filled list and the tracking boolean flag 
                  back to group_management().
"""    
def manage_session_members(session_members):
    
    # Initialice variable with a "not a new group" default value
    new_group = False
    # Present next actions
    print(f"{COLOR_CYAN}============================")
    print ("Let's organize a Game Session!")
    print("============================")
    print(f"Who is comming this time?{COLOR_RESET}")
    answer = str ( input (f"{COLOR_RED}Add player name. [Press 'ENTER' to end]: "))

    while answer != "":

        with open("Players.txt", "r", encoding="utf-8") as file:
            contenido = file.read().splitlines()
            
        if answer not in contenido:
            confirm = input(f"{COLOR_RED}New Player detected. Ok to add {answer} to the list? y/(N) {COLOR_RESET}").strip().lower()
            if confirm == "y":
                with open("Players.txt", "a", encoding="utf-8") as file:
                    print(answer)
                    file.write(answer + "\n")
                    new_group = True
            else:
                print (f"{COLOR_YELLOW}Not added. Let's go on joining players...{COLOR_RESET}")
                answer = ""  #Nothing to be added and while loop will go on.          

        # In other case add members to the list        
        session_members.append(answer)
        print (f"{COLOR_YELLOW}Up to now this members {session_members} entered the session{COLOR_RESET}")
        
        answer = str ( input ("Add player name. [Press 'ENTER' to end]: "))
    
    # Return the list of memebers and a boolean to confirm nextd action.
    return session_members, new_group





if __name__ == "__main__":
    main()




