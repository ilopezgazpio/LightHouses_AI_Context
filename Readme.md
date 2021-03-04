# Fork of lighthouses_aicontest
https://github.com/marcan/lighthouses_aicontest.git

Read file ```aicontest_spec.txt``` for long description of the game.

## Launch configuration
Prepare the environment with conda, see engine readme file
```
conda install --name python3x -c cogsci pygame
conda activate python3x
... launch ai context ...
conda deactivate
```
if this fails, you can try 
```
python3 -m pip install -U pygame --user
```

## Launch the game with one bot
```
python engine/game.py \
--map 'maps/grid.txt' \
--bots 'python examples/RandBot/randbot.py'
```

## Launch the game with N bots
```
python engine/game.py \
--map 'maps/grid.txt' \
--bots 'python examples/RandBot/randbot.py' \
'python examples/RandBot/randbot.py' \
'python examples/RandBot/randbot.py' \
'python examples/RandBot/randbot.py' \
...
'python3.6 bots/RandBot/randbot.py'
```

## Brief description of the game 
- The game consists on programming small artificial intelligence software units (agents) that are launched inside the game as subprocesses.
- The agents aim to collect as many points as possible by conquering lighthouses and conquering land between lighthouses.
- The agents are restricted in time to make decisions that influence the environment

### The map
- 2D world, with no wrapparound
- Left bottom is (0,0), increases positively going right / up

### Energy
- Initially 0
- Computed at each time step accoring to a formula that takes into account proximity to lighthouses
- When agent goes through cell with energy, it collects that energy

### Agents
- 1+, each has a id given by the engine 0..N
- 8 possible directions to move in the board

### Lighthouses
- Can be free or conquered by an agent
- If it is conquered that means some energy had been left there, this energy decreases over time until reaching 0
- When the energy of a lighthouse reaches 0 the agent loses control over it
- Energy can be refilled
- Cells nearby lighthouses collect energy with a formula that takes proximity into account
- Owning lighthouses gives small points to agents

### Connections
- 2 lighthouses can be connected, if owned by the same agent
- Connections can not cross other connections
- Connections can not cross other lighthouses
- To establish a connection agent must be located in a lighthouse and own the key of the remote lighthouse
- Connections give extra points to the agents
- Connections can form triangles, in which case, the agent receives extra points for all the area under the triangle

### Game states - Game start
At game start the engine gives agents the following information encoded as a ```JSON``` message:
- player id
- total number of players
- initial position
- boolean map of the game ( with playable / non playable cells )
- positions for lighthouses 

```
{
	"player_num": 0,
	"player_count": 2,
	"position": [1, 2],
	"map": [
		[0, 0, 0, 0, 0],
		[0, 1, 1, 1, 0],
		[0, 1, 1, 0, 0],
		[0, 1, 1, 0, 0],
		[0, 0, 0, 0, 0]],
	"lighthouses": [
		[1, 1], [3, 1], [2, 3], [1, 3]
	]
}
```

### Game states - Before round start
The following happens every round start, actioned by the game engine
- Cells increase the energy by += floor( constant - distance_to_nearest_lighthouse). Maximum energy es 100.
- If agent is on a cell of a lighthouse, it obtains its key
- Lighthouse energy is decremented in 10

### Game states - Round start
Agent receives the following information at each round:
- Current location
- Score
- Energy available
- A energy map of nearby cells ( distance <= 3)
- Information for each lighthouse (location, owner id, energy, list of connected lighthouses, boolean indicating if agent has the key or not)

```
{
	"position": [1, 3],
	"score": 36,
	"energy": 66,
	"view": [
		[-1,-1,-1, 0,-1,-1,-1],
		[-1, 0, 0,50,23,50,-1],
		[-1, 0, 0,32,41, 0,-1],
		[ 0, 0, 0, 0,50, 0, 0],   
		[-1, 0, 0, 0, 0, 0,-1],   
		[-1, 0, 0, 0, 0, 0,-1],
		[-1,-1,-1, 0,-1,-1,-1]
	],
	"lighthouses": [
		{
			"position": [1, 1],
			"owner": 0,
			"energy": 30,
			"connections": [[1, 3]],
			"have_key": false
		},
		{
			"position": [3, 1],
			"owner": -1,
			"energy": 0,
			"connections": [],
			"have_key": false
		},
		{
			"position": [2, 3],
			"owner": 1,
			"energy": 90,
			"connections": [],
			"have_key": false
		},
		{
			"position": [1, 3],
			"owner": 0,
			"energy": 50,
			"connections": [[1, 1]],
			"have_key": true
		}
	]
}
```

### Agent actions
- Do nothing
```
{
	"command": "pass"
}
```
- Move
```
{
	"command": "move",
	"x": -1,
	"y": 1
}
```

- Conquer / refill lighthouse
```
{
	"command": "attack",
	"energy": 80
}
```

- Connect to other lighthouse
```
{
	"command": "connect",
	"destination": [1, 1]
}
```

- The engine can respond to our requests with
OK response
```
{
	"success": true
}
```
KO response
```
{
	"success": false,
	"message": "Player does not have the destination key"
}
```

### Scoring 
- Initially 0 points
Per round the engine gives the following points
- +2 per lighthouse
- +2 per link
- +1 per cell under triangle

### Communication between the engine and the robot
- Thorugh stdio / stdout
- Based on JSON messages (string must end with '\n')
- If using stderr the agent must identify itself before the message including '[BOTNAME]' prior to the message
- Bot must be destroyed when engine closes ```stdin``` with it (EOF)