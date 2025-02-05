import uuid
import shortuuid
import pandas as pd
import numpy as np

def balanced_group_assignment(df, new_participants, substrings):
    for substring in substrings:
        for _ in range(new_participants):
            tmp_id = uuid.uuid4()
            uuid_ = shortuuid.encode(tmp_id)[:6]
            full_id = substring + uuid_
            new_row = pd.DataFrame({'IDs': [full_id], 'Group': [None], 'Stage': [np.random.randint(1, 4)]})
            df = pd.concat([df, new_row], ignore_index=True)

    # Balance groups based on Stage
    for stage in range(1, 4):
        stage_df = df[df['Stage'] == stage]
        trt_count = stage_df[stage_df['Group'] == 'TRT'].shape[0]
        ctr_count = stage_df[stage_df['Group'] == 'CTR'].shape[0]

        # Assign groups to balance the count
        for index, row in stage_df[stage_df['Group'].isnull()].iterrows():
            if trt_count <= ctr_count:
                df.at[index, 'Group'] = 'TRT'
                trt_count += 1
            else:
                df.at[index, 'Group'] = 'CTR'
                ctr_count += 1

    return df

# Example initial data
data = {
    'IDs': ['AUS_abcdef', 'AUS_bcdefg', 'AUS_cdefgh'],
    'Group': ['TRT', 'CTR', 'TRT'],
    'Stage': [1, 2, 3]
}
df = pd.DataFrame(data)

# Modify the initial data to have a total of 6 examples
current_ids = {
    'IDs': ['AUS_abcdef', 'AUS_bcdefg', 'AUS_cdefgh', 'AUS_ijklmn', 'AUS_mnopqr', 'AUS_opqrstu'],
    'Group': ['TRT', 'CTR', 'TRT', 'TRT', 'CTR', 'TRT',],
    'Stage': [1, 2, 3, 2, 1, 1]
}
df = pd.DataFrame(current_ids)

# Substrings for new IDs
substrings = ['AUS_']
new_participants_per_site = 6  # Example: Add 6 new participants per site

# Generate a balanced DataFrame
balanced_df = balanced_group_assignment(df, new_participants_per_site, substrings)
# Show the median stage for the original data and the balanced data
print("Median H&Y stage for original data:", df['Stage'].mean())
print("Median H&Y stage for balanced data:", balanced_df['Stage'].mean())

