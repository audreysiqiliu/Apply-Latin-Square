import json
import os
import numpy as np
import random

def is_latin_square(square):
    N = len(square)
    for i in range(N):
        if len(set(square[i])) != N or len(set(square[:,i])) != N:
            return False
    return True


def initialize_latin_square(N):
    # Initialize a simple Latin square
    return np.array([(np.arange(N) + i) % N for i in range(N)])

def modify_latin_square(square):
    N = square.shape[0]
    new_square = np.copy(square)

    # Decide randomly to swap rows or columns
    if random.choice([True, False]):
        # Swap two rows
        row1, row2 = np.random.choice(N, 2, replace=False)
        new_square[[row1, row2], :] = new_square[[row2, row1], :]
    else:
        # Swap two columns
        col1, col2 = np.random.choice(N, 2, replace=False)
        new_square[:, [col1, col2]] = new_square[:, [col2, col1]]

    return new_square

def generate_latin_square(N, maxIter=100000, nProper=10):
    latin_square = initialize_latin_square(N)
    proper_count = 0
    proper_squares = []

    for _ in range(maxIter):
        new_square = modify_latin_square(latin_square)
        if is_latin_square(new_square):
            proper_count += 1
            proper_squares.append(new_square)
            latin_square = new_square
            if proper_count >= nProper:
                break
        else:
            print(f"Improper square at iteration {_}.")  # Debugging print

    return proper_squares

def apply_latin_square_to_blocks(blocks, latin_squares):
    all_versions = []
    for square in latin_squares:
        for permutation in square:
            version_blocks = []
            for block_index, block in enumerate(blocks):
                # Create a mapping of original trial order
                original_order = {trial_index: trial for trial_index, trial in enumerate(block['trials'])}

                if block.get('isPractice'):
                    practice_trials = [trial.copy() for trial in block['trials']]
                    version_blocks.append({**block, 'trials': practice_trials})
                else:
                    shuffled_trials = []
                    for new_index, original_index in enumerate(permutation):
                        trial = original_order[original_index].copy()
                        trial['trialID'] = f"{block_index}_{original_index + 1}"
                        shuffled_trials.append(trial)
                    version_blocks.append({**block, 'trials': shuffled_trials})
            all_versions.append(version_blocks)
    return all_versions



# Load the JSON data
file_path = "/Users/audreyliu/Library/CloudStorage/GoogleDrive-audrey.liu@email.gwu.edu/My Drive/Tasks/Helper Functions/Latin Squares/original_exp_struct.json"
output_path = "/Users/audreyliu/Library/CloudStorage/GoogleDrive-audrey.liu@email.gwu.edu/My Drive/Tasks/Helper Functions/Latin Squares/Ts-and-Ls_Burnout_ExpStructs_MCMC/"

with open(file_path, 'r') as file:
    experiment_blocks = json.load(file)

# Find the number of trials in the first non-practice block
experiment_trial_count = next((len(block['trials']) for block in experiment_blocks if not block['isPractice']), None)

# Generate the Latin Squares using MCMC algorithm
latin_squares = generate_latin_square(experiment_trial_count)

# Apply the Latin Squares to the blocks
all_versions = apply_latin_square_to_blocks(experiment_blocks, latin_squares)

def save_versions(versions, output_directory):
    file_paths = []
    for i, version in enumerate(versions):
        filename = f'expStruct_version{i + 1}.json'
        filepath = os.path.join(output_directory, filename)
        print(f"Saving to {filepath}...")  # Debugging print
        with open(filepath, 'w') as f_out:
            json.dump(version, f_out, indent=2)
        file_paths.append(filepath)
    return file_paths

# Save all versions to separate files in the output directory
version_file_paths = save_versions(all_versions, output_path)

# Output the file paths
print("Files saved to the following paths:")
for path in version_file_paths:
    print(path)
