class TeamMember(object):

    _INVALID = "Invalid Request"

    ## Initializes a TeamMember with name, archetype, and coordinates
    # @param name The name of the TeamMember (e.g. "Sam")
    # @param archetype The archetype of the TeamMember (e.g. "Coder")
    # @param location The location that the TeamMember will start in
    def __init__(self, name, archetype, location):

        self.energy = 100
        self.name = name
        self.archetype = archetype #TODO unitType seems like a more natural name to me. - Ace
        self.location = location

    ## Moves the player to the desired room
    # @param Destination The Room to move to
    def move(destination):

        # TODO How will this be worked out visually, pathfinding?
        self.location = destination

    ## Applies the specified table's Food's effects to the team member
    # @param foodTable The FoodTable that the team member eats from
    def eat(foodTable):
        # TODO What stats need to be added/changed?
        self.energy += foodTable.food.energyValue
        foodTable.amount -= 1

    ## Applies the effects of a specified length of sleep to the player
    # @param hours The number of hours the team member sleeps for
    def sleep(hours):
        self.energy += (hours * 15)

    ## Adjusts the team's AI's stats
    # @param attribute The attribute to change
    # @param amount The amount of change it by (need not be positive)
    def code(team, attribute, amount):
        # TODO Why is this not called changeAiAttribute? That makes more sense to me... - Ace
        team.ai.changeAttribute(attribute, amount)


#this is how you can do simple tests
if __name__ == "__main__":
    sam = TeamMember("Sam", "Coder", "2405")
    print sam.energy
    print sam.name
    print sam.archetype
    print sam.location
