class Robot:
    # 1. The Setup (__init__)
    # This runs automatically when you create a bot
    def __init__(self, name, color):
        self.name = name    # "Attach the name to THIS specific bot"
        self.color = color  # "Attach the color to THIS specific bot"

    # 2. A Method (Action)
    def introduce(self):
        # We use 'self.name' to make sure we use the right name
        print(f"I am {self.name} and I am painted {self.color}.")

# --- THE FACTORY FLOOR ---

# Create Robot #1
r1 = Robot("R2D2", "Blue")

# Create Robot #2 (Same class, different data!)
r2 = Robot("C3PO", "Gold")

# Let them speak
r1.introduce()  # Prints: I am R2D2...
r2.introduce()  # Prints: I am C3PO...