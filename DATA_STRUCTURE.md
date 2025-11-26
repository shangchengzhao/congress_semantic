# Data Structure Documentation

## Participant ID System

### How IDs are Generated
Each participant gets a **unique ID** generated when they start the experiment:

**Format:** `P[timestamp]_[random string]`

**Example:** `P1732567890123_a7x3k9m2p`

**Components:**
- `P` = Participant prefix
- `1732567890123` = Unix timestamp (milliseconds since 1970)
- `a7x3k9m2p` = Random 9-character string

### Why This ID System?
- **Unique**: Combination of timestamp + random string ensures no duplicates
- **Traceable**: Timestamp shows when participant started
- **Anonymous**: No personal information
- **Consistent**: Same ID used for all rows of that participant's data

## Data Columns in Google Sheets

### Participant Information
- `participant_id` - Unique identifier for each participant
- `assigned_trial_type` - Which condition (1, 2, or 3) the participant was assigned to

### Trial Information
- `task` - Type of trial: 'rating', 'attention_check', or 'memory_check'
- `stimulus_name` - Name of the candidate
- `trial_type` - Condition for this trial: 'photo', 'bio', or 'dual'
- `block` - Block number (1 or 2)

### Rating Trials (task = 'rating')
- `question` - The main question text
- `familiarity_rating` - 0 or 1 (only in Block 1)
- `rating` - Main question rating (1-7 scale)
- `secondary_rating` - Similarity rating (1-7 scale, only for bio/dual in Block 2)
- `rt` - Response time in milliseconds
- `responded_on_time` - true/false

### Attention Check Trials (task = 'attention_check')
- `correct_response` - The correct key to press
- `response` - What the participant pressed
- `correct` - true/false

### Memory Check Trials (task = 'memory_check')
- `check_question` - The memory question text
- `correct_answer` - Correct answer: "1" (yes) or "0" (no)
- `response` - Participant's response: "1" or "0"
- `correct` - true/false
- `timed_out` - true if participant didn't respond in 10 seconds

## Example Data Rows

### Rating Trial (Block 1)
```
participant_id: P1732567890123_a7x3k9m2p
assigned_trial_type: 2
task: rating
stimulus_name: Adam_Frisch
trial_type: photo
block: 1
question: How good do you think this person would be as a member of congress?
familiarity_rating: 1
rating: 5
secondary_rating: null
rt: 3450
responded_on_time: true
```

### Memory Check Trial
```
participant_id: P1732567890123_a7x3k9m2p
assigned_trial_type: 2
task: memory_check
stimulus_name: Dan_Newhouse
block: 1
check_question: Dan Newhouse received Agricultural Economics Bachelor degree from Washington State University
correct_answer: 1
response: 1
correct: true
timed_out: false
rt: 2340
```

## How to Analyze Data

### Group by Participant
```
Filter by participant_id to get all data from one person
```

### Compare Conditions
```
Filter by assigned_trial_type (1, 2, or 3) to compare experimental conditions
```

### Check Performance
```
Filter task = 'attention_check' or 'memory_check' 
Calculate: % correct per participant
```

### Analyze Ratings
```
Filter task = 'rating'
Group by trial_type (photo, bio, dual)
Compare ratings across conditions
```

## Important Notes

1. **Each participant = One unique ID** across all their trials
2. **Different participants = Different IDs** (no overlap)
3. **Block 1 & 2 memory checks are different trials** (tracked separately)
4. **Trial group order is randomized** each block (photo/bio/dual order varies)
5. **Familiar candidates excluded** from Block 2 (tracked in console)
