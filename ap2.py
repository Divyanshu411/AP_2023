# Reads integers between a given minimum and maximum, using the prompt provided.
def read_integer_between_numbers(prompt, mini, maximum, input_function=input):
    while True:
        try:
            users_input = int(input_function(prompt))
            if mini <= users_input <= maximum:
                return users_input
            else:
                print(f"Numbers from {mini} to {maximum} only.")
        except ValueError:
            print("Sorry, numbers only please.")

# Reads a non-empty, alphabetical string, using the prompt provided.
def read_nonempty_string(prompt):
    while True:
        users_input = input(prompt)
        if len(users_input) > 0 and users_input.isalpha():
            break
        else:
            print("Sorry, string mustn't be empty and must be alphabetical.")
    return users_input

# Reads an integer value greater or equal to 0.
def read_integer(prompt):
    while True:
        try:
            users_input = int(input(prompt))
            if users_input >= 0:
                return users_input
            else:
                print("Sorry, input must be greater or equal to 0.")
        except ValueError:
            print("Sorry, numbers only please.")

# Reads a float value greater or equal to 0.
def read_float(prompt):
    while True:
        try:
            users_input = float(input(prompt))
            if users_input >= 0:
                return users_input
            else:
                print("Sorry, input must be greater or equal to 0.")
        except ValueError:
            print("Sorry, numbers only please.")
            

# Reads the data for the runners from a given file, processes the lines and returns two lists with all the values.
def runners_data():
    with open("Runners-1.txt") as input:
        lines = input.readlines()
    runners_name = []
    runners_id = []
    for line in lines:
        split_line = line.strip().split(",")

        if len(split_line) > 1:
            runners_name.append(split_line[0])
            id = split_line[1]
            runners_id.append(id)
    return runners_name, runners_id


# Displays the results of a race at a given location, selected by the user, and returns the values.
def race_results(races_location):
    for i in range(len(races_location)):
        print(f"{i+1}: {races_location[i]}")
    user_input = read_integer_between_numbers("Choice > ", 1, len(races_location))
    venue = races_location[user_input - 1]
    id, time_taken = reading_race_results(venue)
    return id, time_taken, venue


# Reads the data for race venues from a given file, processes the lines, and returns a list with all the values.
def race_venues():
    with open("Races-1.txt") as input:
        lines = input.readlines()
    races_location = []
    races_targettime = []
    for line in lines:
        split_line = line.strip().split(",")
        if len(split_line) > 1:
            races_location.append(split_line[0])
            races_targettime.append(float(split_line[1].strip()))
    return races_location, races_targettime


# Returns the winner of a given race.
def winner_of_race(id, time_taken):
    quickest_time = min(time_taken)
    winner = ""
    for i in range(len(id)):
        if quickest_time == time_taken[i]:
            winner = id[i]
    return winner


# Displays the results of a race and the winner of said race.
def display_races(id, time_taken, venue, fastest_runner):
    print(f"Results for {venue}")
    print(f"="*37)
    minutes = []
    seconds = []
    for i in range(len(time_taken)):
        minute, second = convert_time_to_minutes_and_seconds(time_taken[i])
        minutes.append(minute)
        seconds.append(second)
    for i in range(len(id)):
        print(f"{id[i]:<10s} {minutes[i]} minutes and {seconds[i]} seconds")
    print(f"{fastest_runner} won the race.")


# Takes a user input for a new race, noting its location, the times each racer took, and saves these to a file.
def users_venue(races_location, races_targettime, runners_id):
    while True:
        user_location = read_nonempty_string("Where will the new race take place? ").capitalize()
        if user_location not in races_location:
            break
        else:
            print("Input new locations only.")

    while True:
        user_targettime = read_float("What will the target time for this new race be? ")
        if user_targettime not in races_targettime:
            break
        else:
            print("Input new locations only.")

    connection = open(f"{user_location}.txt", "w")
    races_location.append(user_location)
    races_targettime.append(user_targettime)
    time_taken = []
    updated_runners = []
    for i in range(len(runners_id)):
        time_taken_for_runner = read_integer(f"Time for {runners_id[i]} >> ")
        if time_taken_for_runner != 0:
            time_taken.append(time_taken_for_runner)
            updated_runners.append(runners_id[i])
            print(f"{runners_id[i]},{time_taken_for_runner}", file=connection)
    connection.close()


# Updates the races file with new race information.
def updating_races_file(races_location, races_targettime):
    connection = open(f"Races-1.txt", "w")
    for i in range(len(races_location)):
        print(f"{races_location[i]}, {races_targettime[i]}", file=connection)
    connection.close()


# Displays competitors by county, for each county in the county codes file.
def competitors_by_county(name, id):
    with open("County_codes-1.txt") as input:
        lines = input.readlines()
    county_names = []
    county_codes = []
    for line in lines:
        split_line = line.split(",")
        if len(split_line) > 1:
            county_names.append(split_line[0].strip())
            county_codes.append(split_line[1].strip())
    for i in range(len(county_names)):
        print(f"\n{county_names[i]} runners")
        print("=" * 20)
        for j in range(len(name)):
            if id[j].startswith(county_codes[i]):
                print(f"{name[j]} ({id[j]})")


# Reads race results from the corresponding race's file and returns racers and their times taken.
def reading_race_results(location):
    with open(f"{location}.txt") as input_type:
        lines = input_type.readlines()
    id = []
    time_taken = []
    for line in lines:
        line = line.strip()
        if line != "":
            split_line = line.split(",".strip("\n"))
            id.append(split_line[0])
            time_taken.append(int(split_line[1].strip("\n")))
    return id, time_taken


# Reads race results of a specific runner, according to their id, at a given location.
def reading_race_results_of_relevant_runner(location, runner_id):
    with open(f"{location}.txt") as input_type:
        lines = input_type.readlines()
    id = []
    time_taken = []
    for line in lines:
        line = line.strip()
        if line != "":
            split_line = line.split(",".strip("\n"))
            id.append(split_line[0])
            time_taken.append(int(split_line[1].strip("\n")))
    for i in range(len(id)):
        if runner_id == id[i]:
            time_relevant_runner = time_taken[i]
            return time_relevant_runner
    return None


# Goes through all race results and displays only those who have won at least one race.
def displaying_winners_of_each_race(races_location):
    print("Venue             Winner")
    print("="*24)
    for i in range(len(races_location)):
        id, time_taken = reading_race_results(races_location[i])
        fastest_runner = winner_of_race(id, time_taken)
        print(f"{races_location[i]:<18s}{fastest_runner}")


# Displays all runners and takes a user input to print information about the selected runner.
def relevant_runner_info(runners_name, runners_id):
    for i in range(len(runners_name)):
        print(f"{i + 1}: {runners_name[i]}")
    user_input = read_integer_between_numbers("Which Runner > ", 1, len(runners_name))
    runner = runners_name[user_input - 1]
    id = runners_id[user_input -1]
    return runner, id


# Converts minutes to seconds and returns both the minutes and the remainder.
def convert_time_to_minutes_and_seconds(time_taken):
    MINUTE = 60
    minutes = time_taken // MINUTE
    seconds = time_taken % MINUTE
    return minutes, seconds


# Gets a location, creates an organized list of all the final times, and finds where a given time placed.
def sorting_where_runner_came_in_race(location, time):
    with open(f"{location}.txt") as input_type:
        lines = input_type.readlines()
    time_taken = []
    for line in lines:
        split_line = line.split(",".strip("\n"))
        if len(split_line) > 1:
            t = int(split_line[1].strip("\n"))
            time_taken.append(t)

    time_taken.sort()
    return time_taken.index(time) + 1, len(lines)


# Displays the races time of a given competitor at all venues, also displaying the position they finished in.
def displaying_race_times_one_competitor(races_location, runner, id):
    print(f"{runner} ({id})")
    print(f"-"*35)
    for i in range(len(races_location)):
        time_taken = reading_race_results_of_relevant_runner(races_location[i], id)
        if time_taken is not None:
            minutes, seconds = convert_time_to_minutes_and_seconds(time_taken)
            came_in_race, number_in_race = sorting_where_runner_came_in_race(races_location[i], time_taken)
            print(f"{races_location[i]} {minutes} mins {seconds} secs ({came_in_race} of {number_in_race})")


# Given the time of the fastest runner, returns the runner's name.
def finding_name_of_winner(fastest_runner, id, runners_name):
    runner = ""
    for i in range(len(id)):
        if fastest_runner == id[i]:
            runner = runners_name[i]
    return runner


# Goes through all locations and finds the winner of each. The winners are then added to a list and displayed.
def displaying_runners_who_have_won_at_least_one_race(races_location, runners_name, runners_id):
    print(f"The following runners have all won at least one race:")
    print(f"-" * 55)
    winners = []
    runners = []
    for i, location in enumerate(races_location):
        id, time_taken = reading_race_results(location)
        fastest_runner = winner_of_race(id, time_taken)
        name_of_runner = finding_name_of_winner(fastest_runner, runners_id, runners_name)
        if fastest_runner not in winners:
            winners.append(fastest_runner)
            runners.append(name_of_runner)
    for i, fastest_runner in enumerate(winners):
        print(f"{runners[i]} ({fastest_runner})")


# Main function of the code, does initial file reading, takes user input for desired functioning, and exits once the user is finished.
def main():
    parser = argparse.ArgumentParser(description='Race Information System')
    parser.add_argument('menu_option', type=int, choices=range(1, 8), help='Menu option number (1-7)')
    args = parser.parse_args()

    races_location, races_targettime = race_venues()
    runners_name, runners_id = runners_data()

    if args.menu_option == 1:
        id, time_taken, venue = race_results(races_location)
        fastest_runner = winner_of_race(id, time_taken)
        display_races(id, time_taken, venue, fastest_runner)
    elif args.menu_option == 2:
        users_venue(races_location, races_targettime, runners_id)
    elif args.menu_option == 3:
        competitors_by_county(runners_name, runners_id)
    elif args.menu_option == 4:
        displaying_winners_of_each_race(races_location)
    elif args.menu_option == 5:
        runner, id = relevant_runner_info(runners_name, runners_id)
        displaying_race_times_one_competitor(races_location, runner, id)
    elif args.menu_option == 6:
        displaying_runners_who_have_won_at_least_one_race(races_location, runners_name, runners_id)
    else:
        updating_races_file(races_location, races_targettime)

if __name__ == '__main__':
    main()
