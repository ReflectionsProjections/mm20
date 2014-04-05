class TeamMember(object):

    _INVALID = "Invalid Request"

    ## Initializes a TeamMember with name, archetype, and coordinates
    # @param name The name of the TeamMember (e.g. "Sam")
    # @param archetype The archetype of the TeamMember (e.g. "Coder")
    # @param location The location that the TeamMember will start in
    def __init__(self, name, archetype, location, team):

        self.energy = 100
        self.name = name
        self.archetype = archetype #TODO Archetypes should be defined in constants along with characteristics
        self.location = location
        self.team = team

    ## Moves the player to the desired room
    # @param Destination The Room to move to
    def move(self, destination):

        # TODO How will this be worked out visually, pathfinding?
        self.location = destination

    ## Applies the specified table's Food's effects to the team member
    # @param foodTable The FoodTable that the team member eats from
    def eat(self, foodTable):
        # TODO What stats need to be added/changed?
        self.energy += foodTable.food.energyValue
        foodTable.amount -= 1

    ## Applies the effects of a specified length of sleep to the player
    # @param hours The number of hours the team member sleeps for
    def sleep(self, hours):
        self.energy += (hours * 15)

    ## Adjusts the team's AI's stats
    # @param attribute The attribute to change
    # @param amount The amount of change it by (need not be positive)
    def code(self, team, attribute):

        # TODO 10 should be loaded from a constants file and should be based on the attribute.
        # e.g the amount of change whe working on optimization might be diffent from stability
        # Also this will be based on a funtion that take time spent and player attributes into consderaion
        
        
        team.ai.changeAttribute(attribute, 10)


#this is how you can do simple tests
if __name__ == "__main__":
    sam = TeamMember("Sam", "Coder", "2405")
    print sam.energy
    print sam.name
    print sam.archetype
    print sam.location
