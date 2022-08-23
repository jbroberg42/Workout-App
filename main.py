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
        print("\n\n\nAvailable Profiles:")
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
        user_input = input("\nWhat would you like to do? > ").lower()
        match user_input:
            case 'c':
                print('\n\n\nCreating new profile...')
                sql.add_profile(input('\nEnter new profile name:\n> '))

            case 'd':
                print('\n\n\nDeleting profile...')
                for profile in existing_profiles:
                    print("[{}] --> {}".format(profile[0], profile[1]))
                selected_id = get_int('\nEnter id of profile to delete.')
                if selected_id in available_ids:
                    profile_to_delete = Profile(selected_id)
                    if get_conf("\n\n\nAre you sure you would like to delete  {} ? You cannot undo this action.".format(profile_to_delete.name)):
                        sql.del_profile(profile_to_delete.name)
                else:
                    print('\n\n\nError: Profile with that id does not exist.')
            case 'o':
                for profile in existing_profiles:
                    print("[{}] --> {}".format(profile[0], profile[1]))
                selected_id = input('\nPlease select the id of desired profile. > ')
                if selected_id in available_ids:

                    global current_profile
                    current_profile = Profile(selected_id)
                    
                    break
                else:
                    print('\n\n\nSorry, that profile does not exist.')
            case _:
                print("\n\n\nPlease input a valid command.")



def user_menu():
    while True:
        print("\n\n\n[A]dd set")
        print("[V]iew existing sets")
        print("[E]xit")
        match input("\nWhat would you like to do? > ").lower():
        
# prompt the user to select from or add to the exercise SQL table
            case 'e':
                break
            case 'a':
                print('\n\n\nAdding set...\n\n\nSelect exercise:')
                available_exercise_ids = []
                for type in sql.list_exercise_types():
                    available_exercise_ids.append(type[0])
                    print("[{}] --> {}".format(type[0], type[1]))
                print('[A]dd new exercise')
                print("[B]ack")
                while True:
                    user_input = input("> ").lower()
                    match user_input:
                        case 'b':
                            break
                        case 'a':
                            sql.add_exercise_type(input('\n\n\nEnter name of new exercise: > '))
                            break
                        case _:
                            if int(user_input) in available_exercise_ids:
                                selected_exercise_id = user_input
                                set_input = input('\n\n\nEnter set information:\n(Use syntax: [SET]x[REPS]x[WEIGHT])\n\n> ')
                                sets_count, reps_count, weight = set_input.strip().split('x')
                                for i in range(int(sets_count)):
                                    sql.add_set(current_profile.id, reps_count, selected_exercise_id, weight, current_date)
                                print('\n\n\nSet successfully added!')
                                break
                            else:
                                print('\n\n\nPlease enter a valid command.')
            

# allow the user to view their history
            case 'v':
                while True:
                    print('\n\n\nView [A]ll')
                    print('[F]ilter by exercise')
                    print('[B]ack')
                    user_input = input("> ").lower()
                    match user_input:
                        case 'a':
                            profile_sets = sql.list_sets(current_profile.id)
                            for set in profile_sets:
                                x, reps, exercise_id, weight, date = set
                                print(f"{date}: {sql.get_exercise_type(exercise_id)[0]}, {weight}lbs, {reps} reps")
                        case 'f':
                            while True:
                                print('\n\n\nSelect exercise to view history:')
                                available_exercise_ids = []
                                for type in sql.list_exercise_types():
                                    available_exercise_ids.append(type[0])
                                    print("[{}] --> {}".format(type[0], type[1]))
                                try:    
                                    user_input = int(input("> "))
                                    if user_input in available_exercise_ids:
                                        profile_sets = sql.list_sets(current_profile.id, user_input)
                                        print('\n\n\nShowing all: ' + sql.get_exercise_type(user_input)[0])
                                        for set in profile_sets:
                                            x, reps, exercise_id, weight, date = set
                                            print(f"{date}: {weight}lbs, {reps} reps")
                                        break
                                    else:
                                        print('\n\n\nPlease enter a valid exercise id.')
                                except ValueError:
                                        print('\n\n\nPlease enter a valid exercise id.')
                        case 'b':
                            break
                        case _:
                            print("\n\n\nPlease enter a valid command.")



global current_profile

if __name__ == "__main__":
    # Check if there is a database called 'workout_app.db' in the current directory and creates one if not found.
    sql.create_database()

    # Run the startup menu and allow users to login to, create, or delete profiles.
    print("\n\n\nWelcome to Jonah's Workout App!")
    startup_menu()

    # Greet the user.
    print("\n\n\nHi, " + current_profile.name + "!")
    
    # Run the user menu and allow users to add, view, or delete sets.
    user_menu()
    