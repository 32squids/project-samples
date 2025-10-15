import numpy as np
import gymnasium as gym

"""This is an ML algorithm that uses Markov models to play Kiri-Ai: The Duel. The model is based on a rock-paper-scissors-like
game with a few twists. In the original game, players play as dueling samurai. Players may advance, retreat, attack, or change
stances. Hit your opponent twice to win! Over time, the model will be made more complicated to accommodate all these extra rules.
For now, there is one agent and one target, no stance changing, one kind of attack, and only one hit to win."""

class BoardState(gym.Env):

    def __init__(self, size: int=2):
        # Currently unused. Can be implemented later to include a more complicated board, an additional stance, etc.
        # self.size = size

        # 'Uninitialized' positions
        self._agent_location = np.array([-1, -1], dtype=np.int32)
        self._target_location = np.array([-1, -1], dtype=np.int32)

        # Build observation space
        self.observation_space = gym.spaces.dict(
            {
                "agent": gym.spaces.Discrete(5, dtype=np.int32), # 5 positions on the board
                                                                 # TODO: 2 statuses for agent and opponent: hit or not hit.
                                                                 # TODO: 2 stances for agent and opponent: heaven or earth
                "target": gym.spaces.Discrete(5, dtype=np.int32) # 5 positions on the board
            }
        )

        # Move forward 1 or 2, retreat 1, or attack.
        # TODO: Allow 2 actions, change stance, earth, neutral, and sky attacks
        self.action_space = gym.spaces.Discrete(4)

        self._action_to_direction = {
            0: np.array([2, 0]), # Charge forward 2
            1: np.array([1, 0]), # Approach 1
            2: np.array([-1, 0]), # Retreat 1
            3: np.array([0, np.random.choice(2)]) # Attack. Random chance of hitting.
                                                  # TODO: Ensure actions are appropriately %ed so second value in {0, 1}
            # 4: np.array([0, 0, np.random.choice([0, 1])]), # Opponent has a random chance of being hit. If they're hit the second time,
            #                                                # they lose. TODO: Implement tracking stances for effective attacks
            # 5: np.array([0, 0, np.random.choice([0, 1])]),
            # 6: np.array([0, 0, np.random.choice([0, 1])])
        }