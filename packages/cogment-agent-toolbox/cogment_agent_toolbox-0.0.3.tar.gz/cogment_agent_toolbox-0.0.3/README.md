# Agent Toolbox

## Overview
The agent toolbox provides for the Environment a way to specify meta data in on the proto file. This helps to provide specification for the tensor. It is not mandatory to use meta_data to be compatible with the tools provided for the agents.

This tool generates tensors from the observation and action space. 

## Setup
```bash
pip install cogment_agent_toolbox
```

## On the Environment side

- Include meta_data.proto in your own proto
- Add the following metadata for the following : 
    - To remove some field from the tensor add the **exclude_from_tensor** metadata aside it :
    ```proto
    [(meta_data.exclude_from_tensor) = true]
    ```
    for instance if you have a field 
    ```proto
    float orientation = 1;
    ```

    replace it by the following line: 
    ```proto
    float orientation = 1 [(meta_data.exclude_from_tensor) = true];
    ```

    - The same way you can specify **min** or **max**, or both : 
    ```proto
    [(meta_data.min) = -1.0, (meta_data.max) = 1.0]
    ```

    - It is also possible to specify an **increment**: 
    ```proto
    float angle = 1 [(meta_data.min) = -3.14159, (meta_data.max) = 3.14159, (meta_data.increment) = 0.3];
    ```


    - It is also possible to provide a hint on how many the repeated field could be used with **repeated_count_hint**: 
    ```proto
    [(meta_data.repeated_count_hint) = 3]
    ```


## On the Agent side

### Import TensorGenerator class in your agent

- Create a generator
```python
from agent_toolbox.tensor_generator import TensorGenerator
generator = TensorGenerator()
```

- Get the action size and observation size of the environment. These functions are uselfull to create the neural net with the right sizes.
```python
generator = TensorGenerator()
state_size = generator.get_state_size()
action_size = generator.get_action_size()
```

- Compute state tensor from the environment observation or compute action tensor from an environment action 
```python
state = generator.compute_tensor(obs)
```

- Compute action from a tensor, useful function when the type of action  is continuous
```python
action_from_tensor = generator.compute_action_from_tensor(action_tensor)
```

### Discrete Actions utils

- Consult all possible actions generated for a classification problem
```python
generator.get_possible_actions()
```
- Returns the number of actions generated for a classification problem 
```python
classification_size = generator.get_classification_size()
```
equivalent to 
```python
len(generator.get_possible_actions())
```

- Compute a choice for a classification problem, from an action tensor. The returned value is an index in the possible action list. 
```generator.get_possible_actions()```
```python
choice = generator.compute_choice_from_action(action_tensor)
```

- Convert the selected action index in action required by the environment. The parameter ```choice``` is an index from 0 to n,
 n being ```generator.get_classification_size()```. 
```python
generator.convert_choice_in_action(choice)
```

### Examples
- Using action tensor directly, useful for continuous action type.
```python
from agent_toolbox.tensor_generator import TensorGenerator

...

    def decide(self, observation: cog_settings.actor_classes._otsa.observation_space):

        # Create generator
        generator = TensorGenerator()

        # Transform the observation space in tensor
        obs_tensor = generator.compute_tensor(observation)
        print("Observation tensor: ", obs_tensor)

        # Pick an action from a tensor
        action_size = generator.get_action_size()
        action_tensor = [random.random() for i in range(action_size)]

        # Transform the tensor in action
        action_from_tensor = generator.compute_action_from_tensor(action_tensor)

        print("Action from tensor : ", action_from_tensor)
```

- Solving classification problem by using a list generated actions, useful for discrete action type.
```python

    def decide(self, observation: cog_settings.actor_classes._otsa.observation_space):

        # Create generator
        generator = TensorGenerator()

        # Transform the observation space in tensor
        obs_tensor = generator.compute_tensor(observation)
        print("Observation tensor: ", obs_tensor)

        # Pick an action from a classification problem
        classification_size = generator.get_classification_size()
        action_choice = random.randrange(classification_size)

        # Transform the choice in action
        action_from_choice = generator.convert_choice_in_action(
            action_choice)

        print("Action from choice : ", action_from_choice)

```

