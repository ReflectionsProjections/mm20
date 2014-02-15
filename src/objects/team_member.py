class TeamMember(object):

    def __init__(self, name, archetype):
        self.energy = 100
        self.name = name
        self.archetype = archetype


#this is how you can do simple tests
if __name__ == "__main__":
    sam = TeamMember(70)
    print sam.energy