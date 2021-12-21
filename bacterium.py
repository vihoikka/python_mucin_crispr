class Bacterium:
    """A single bacterium"""

    def __init__(self):
        self.model = model
        self.hasSpacer = False
        self.morphotype = "rhizoid"
        self.virulent = True


class Model:
    max_bacteria = 10000

    def __init__(self):
        self.bacteria = {}


timesteps = 600
n = 10000
bacs = []

#create bacteria and store them in list
for i in range(n):
    bac = Bacterium()
    bacs.append(bac)
print("Created " + n + " bacteria")

for i in range(timesteps):
    for b in bacs:
        print(b)
