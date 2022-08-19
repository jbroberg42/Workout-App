from ast import match_case
import sqlfunctions as sql
import datetime
import time

current_date = datetime.date.today()


# Y/N returns True or False
def get_conf(prompt):
    while True:
        confirm = False
        yn = input(f'{prompt} (Y/N) > ').upper()
        if yn == 'Y':
            confirm = True
            break
        elif yn == 'N':
            confirm = False
            break
        else:
            print('Please enter [Y]es or [N]o.')
            continue
    return confirm


# Gets an int and doesn't let user enter anything else
def get_int(prompt):
    while True:
        output = 0
        try:
            output = int(input(f'{prompt} > '))
            break
        except ValueError:
            print('\nInput must be an integer.')
            continue
    return output


# Gets one char and doesn't let user enter anything else
def get_char(prompt):
    while True:
        output = input(f'{prompt} > ')
        if len(output) == 1:
            break
        else:
            print('\nInput must be one character.')
            continue
    return output


def wait():
    time.sleep(1)


class Profile:
    def __init__(self, id, name=None):
        self.id = id
        if name == None:
            self.name = sql.get_profile_name(self.id)
        else:
            self.name = name

    def get_name(self):
        return self.name

    def change_name(self, new_name):
        self.name = new_name

    def get_id(self):
        return self.id

    def change_id(self, new_id):
        self.id = new_id


# opens the user menu, returns the id of the profile that user has selected
def startup_menu():
    # list existing profiles, take input for the profile id, make sure input is valid and change the selected_id
    selected_id = int
    while True:
        # list menu of available actions
        available_ids = []
        print("\nAvailable Profiles:")
        existing_profiles = sql.list_all_profiles()
        for profile in existing_profiles:
            available_ids.append(profile[0])
            print("--> {}".format(profile[1]))
        if len(available_ids) == 0:
            print("--> No profiles currently exist.")
        print("[O]pen existing profile")
        print("[C]reate new profile")
        print("[D]elete existing profile")

        # select profile, create a new one, or delete one
        user_input = get_char("\nWhat would you like to do?\n").lower()
        match user_input:
            case 'c':
                print('Creating new profile...\n')
                sql.add_profile(input('Enter new profile name:\n> '))

            case 'd':
                print('Deleting profile...')
                for profile in existing_profiles:
                    print("[{}] --> {}".format(profile[0], profile[1]))
                selected_id = get_int('\nEnter id of profile to delete:\n ')
                if selected_id in available_ids:
                    profile_to_delete = Profile(selected_id)
                    if get_conf("Are you sure you would like to delete  {} ?".format(profile_to_delete.name)):
                        sql.del_profile(profile_to_delete.name)
                else:
                    print('\nError: Profile with that id does not exist.\n')
            case 'o':
                for profile in existing_profiles:
                    print("[{}] --> {}".format(profile[0], profile[1]))
                selected_id = get_int('\nPlease select the id of desired profile.\n')
                if selected_id in available_ids:

                    global current_profile
                    current_profile = Profile(selected_id)
                    
                    break
                else:
                    print('\nSorry, that profile does not exist.')
            case _:
                print("Please input a valid command.")



def user_menu():
    while True:
        print("[A]dd set")
        print("[V]iew existing sets")
        match input("\nWhat would you like to do?\n").lower():
        
# prompt the user to select from or add to the exercise SQL table
            case 'a':
                while True:
                    print('Adding set...\n\nSelect exercise:')
                    available_exercise_ids = []
                    for type in sql.list_exercise_types():
                        available_exercise_ids.append(type[0])
                        print("[{}] --> {}".format(type[0], type[1]))
                    print('[A]dd new exercise\n')
                    user_input = input("> ").lower()
                    match user_input:
                        case 'a':
                            sql.add_exercise_type(input('Enter name of new exercise: > '))
                        case _:
                            if int(user_input) in available_exercise_ids:
                                selected_exercise_id = user_input
                                set_input = input('Enter set information.\nSYNTAX: [SET]x[REPS]x[WEIGHT]\n\n> ')
                                #try:
                                sets_count, reps_count, weight = set_input.strip().split('x')
                                for i in range(int(sets_count)):
                                    sql.add_set(current_profile.id, reps_count, selected_exercise_id, weight, current_date)
                                print(sql.list_sets(current_profile.id))
                                #except:
                            else:
                                print('Please enter a valid command.\n')
            

# allow the user to view their history
            case 'v':
                print('viewing existing sets..')



global current_profile

if __name__ == "__main__":
    # Check if there is a database called 'workout_app.db' in the current directory and creates one if not found.
    sql.create_database()

    # Run the startup menu and allow users to login to, create, or delete profiles.
    startup_menu()

    # Greet the user.
    print("\n\nHi, " + current_profile.name + "!\n\n")
    
    # Run the user menu and allow users to add, view, or delete sets.
    user_menu()
    