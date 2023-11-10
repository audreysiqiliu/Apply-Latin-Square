from itertools import islice
import json
import os

def create_latin_square(size):
    # This function creates a Latin Square for a given size
    return [[(j + i) % size for j in range(size)] for i in range(size)]

def apply_latin_square_to_blocks(blocks, latin_square):
    # Apply the Latin Square to the experiment blocks and return all versions
    all_versions = []
    for permutation in latin_square:
        version_blocks = []
        for block_index, block in enumerate(blocks):
            if block.get('isPractice'):
                # Copy practice blocks directly and assign IDs
                practice_trials = []
                for trial_index, trial in enumerate(block['trials']):
                    trial_copy = trial.copy()  # Make a copy of the trial
                    # Create a trialID in the format "blockIndex_trialIndex"
                    trial_copy['trialID'] = f"{block_index}_{trial_index + 1}"  # +1 to start trial numbering at 1
                    practice_trials.append(trial_copy)
                version_blocks.append({**block, 'trials': practice_trials})
            else:
                # Apply the permutation to experiment blocks
                shuffled_trials = []
                for trial_index, i in enumerate(permutation):
                    trial = block['trials'][i].copy()  # Make a copy of the trial
                    # Create a trialID in the format "blockIndex_trialIndex"
                    trial['trialID'] = f"{block_index}_{trial_index + 1}"  # +1 to start trial numbering at 1
                    shuffled_trials.append(trial)
                version_blocks.append({**block, 'trials': shuffled_trials})
        all_versions.append(version_blocks)
    return all_versions

file_path = "/Users/audreyliu/Library/CloudStorage/GoogleDrive-audrey.liu@email.gwu.edu/My Drive/Tasks/Helper Functions/original_exp_struct.json"
output_path = "/Users/audreyliu/Library/CloudStorage/GoogleDrive-audrey.liu@email.gwu.edu/My Drive/Tasks/Helper Functions/Ts-and-Ls_Burnout_ExpStructs"

# Load the JSON data
with open(file_path, 'r') as file:
    experiment_blocks = json.load(file)

# Find the number of trials in the first non-practice block
experiment_trial_count = next((len(block['trials']) for block in experiment_blocks if not block['isPractice']), None)
size = experiment_trial_count

# Create the Latin Square
latin_square = create_latin_square(size)

# Apply the Latin Square to the blocks
all_versions = apply_latin_square_to_blocks(experiment_blocks, latin_square)

# Function to save each version to a separate JSON file
def save_versions(versions, output_directory):
    file_paths = []
    for i, version in enumerate(versions):
        filename = f'expStruct_version{i + 1}.json'
        filepath = os.path.join(output_directory, filename)
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
