class TeamMember(object):

    def __init__(self,  energy):
        self.energy = energy
        
#this is how you can do simple tests
if __name__ == "__main__":
    sam = TeamMember(70)
    print sam.energy
    
