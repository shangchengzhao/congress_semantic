# Data Fields Documentation

This document describes all the data fields that are saved from the experiment.

## Global Fields (Added to All Trials)

These fields appear in every row of the data:

1. **participant_id** - Unique identifier for each participant (e.g., "P1764179556092_5bdom9byy")
2. **experiment_start_time** - Human-readable timestamp when experiment started (e.g., "11/26/2025, 14:32:15")
3. **assigned_trial_type** - Randomly assigned condition (1, 2, or 3) for trial type assignment

## jsPsych Standard Fields

These are automatically recorded by jsPsych for every trial:

- **trial_type** - Type of jsPsych plugin used (e.g., "html-keyboard-response", "instructions", "preload")
- **trial_index** - Sequential number of the trial in the experiment
- **time_elapsed** - Milliseconds since experiment start
- **internal_node_id** - jsPsych's internal timeline tracking
- **rt** - Reaction time in milliseconds (time from stimulus onset to response)

## Task-Specific Fields

### For All Task Trials:
- **task** - Type of task (see below for options)
- **block** - Block number (1 or 2)

### Fixation Trials (task = "fixation"):
- No additional fields beyond global and standard fields

### Stimulus Presentation Trials (task = "stimulus_presentation"):
- **stimulus_name** - Name of the candidate (e.g., "Adam_Frisch")
- **stimulus_trial_type** - Type of trial: "photo", "bio", or "dual"
- **question** - The main question text shown for rating

### Rating Trials (task = "rating"):
- **stimulus_name** - Name of the candidate
- **stimulus_trial_type** - Type of trial: "photo", "bio", or "dual"
- **question** - The main question text
- **secondary_question** - The similarity question text (null if not shown)
- **familiarity_rating** - Response to familiarity question: "0" (unfamiliar) or "1" (familiar), or null if not shown
- **main_rating** - Response to main question (1-7 scale value)
- **similarity_rating** - Response to similarity question (1-7 scale value), or null if not shown
- **reaction_time_ms** - Same as rt field, time to respond in milliseconds
- **response_time_limit_ms** - The time limit for responding (20000ms for photo, 120000ms for bio/dual)
- **responded_on_time** - Boolean: true if responded within time limit

### Attention Check Trials (task = "attention_check"):
- **stimulus_name** - null (not applicable for attention checks)
- **stimulus_trial_type** - null (not applicable for attention checks)
- **correct_response** - The key that should have been pressed (e.g., "3")
- **response** - The key that was actually pressed
- **correct** - Boolean: true if response matched correct_response
- **reaction_time_ms** - Time to respond in milliseconds

### Attention Check Feedback (task = "attention_check_feedback"):
- **block** - Block number
- No response data (just displays feedback)

### Memory Check Trials (task = "memory_check"):
- **stimulus_name** - Name of the candidate being checked
- **stimulus_trial_type** - Type of trial: "bio" or "dual"
- **check_question** - The memory check question text
- **correct_answer** - The correct answer: "0" (No) or "1" (Yes)
- **response** - The participant's answer: "0" or "1", or null if timed out
- **correct** - Boolean: true if response matched correct_answer
- **timed_out** - Boolean: true if participant didn't respond in time (10 seconds)
- **reaction_time_ms** - Time to respond in milliseconds

### Memory Check Feedback (task = "memory_check_feedback"):
- **block** - Block number
- No response data (just displays feedback)

## Data Analysis Tips

### To filter for actual rating responses:
```javascript
data.filter(row => row.task === 'rating')
```

### To filter for Block 1 ratings:
```javascript
data.filter(row => row.task === 'rating' && row.block === 1)
```

### To filter for photo trials only:
```javascript
data.filter(row => row.task === 'rating' && row.stimulus_trial_type === 'photo')
```

### To check attention check performance:
```javascript
const attentionChecks = data.filter(row => row.task === 'attention_check');
const accurateAttention = attentionChecks.filter(row => row.correct === true).length;
const attentionAccuracy = accurateAttention / attentionChecks.length;
```

### To check memory check performance:
```javascript
const memoryChecks = data.filter(row => row.task === 'memory_check');
const accurateMemory = memoryChecks.filter(row => row.correct === true).length;
const memoryAccuracy = accurateMemory / memoryChecks.length;
```

### To identify participants who responded too slowly:
```javascript
const slowResponses = data.filter(row => row.task === 'rating' && row.responded_on_time === false);
```

### To get familiarity data (Block 1 only):
```javascript
const familiarityData = data.filter(row => row.task === 'rating' && row.block === 1 && row.familiarity_rating !== null);
```

### To get similarity ratings (Block 2, bio/dual trials only):
```javascript
const similarityData = data.filter(row => 
  row.task === 'rating' && 
  row.block === 2 && 
  row.similarity_rating !== null &&
  (row.stimulus_trial_type === 'bio' || row.stimulus_trial_type === 'dual')
);
```
