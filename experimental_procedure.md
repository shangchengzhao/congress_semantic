# Congressional Candidate Social Impression Rating Experiment

## Experimental Procedure Documentation

---

## Overview
This experiment measures social impressions of congressional candidates across two dimensions: congressional competence and voting intention. Participants view candidate information (photos, biographical text, or both) and provide ratings on 7-point scales. Participants are randomly assigned to one of five participant groups (1-5) and one of three trial type conditions that determine which stimuli are shown and how they are presented (photo/bio/dual) throughout the experiment.

---

## 1. Fixation Cross

### Parameters:
- **Duration**: 500ms (0.5 seconds)
- **Display**: Plus sign (+)
- **Font Size**: 60px
- **Position**: Centered on screen (both horizontally and vertically)
- **Color**: Black on white background
- **Timing**: Presented before each trial (stimulus presentation)

### Purpose:
Alerts participants to focus attention on the center of the screen before stimulus presentation.

---

## 2. Time Limitations

### Stimulus Presentation Time:
- **Photo trials**: 2 seconds (2000ms)
- **Bio trials**: 10 seconds (10000ms)
- **Dual trials**: 10 seconds (10000ms)

### Response Time Limits:
- **Photo trials**: 20 seconds (20000ms)
- **Bio trials**: 120 seconds (120000ms)
- **Dual trials**: 120 seconds (120000ms)

### Actual Response Pace (according to Pilot Data): 
- bio: 20 sec (after 10sec viewing)
- dual: 22sec (after 10sec viewing)
- photo: 5 sec (after 2sec viewing)

### Warning System:
- **Trigger**: Warning message appears if participant does not respond within the time limit
- **Message**: "Please respond faster!"
- **Display**: Red text, appears above the stimulus during rating phase
- **Purpose**: Encourages timely responses without forcing early termination

---

## 3. Stimulus Size

### Image Dimensions:
- **Maximum Width**: 180 pixels
- **Maximum Height**: 220 pixels
- **Aspect Ratio**: Preserved (images scale proportionally)
- **Format**: JPEG or PNG

### Bio Text Box:
- **Maximum Width**: 800 pixels
- **Text Alignment**: Left-aligned
- **Font**: Default sans-serif
- **Line Height**: Default

### Positioning:
- **Initial Presentation**: Stimulus (image/bio/both) centered on screen
- **Rating Phase**: Stimulus remains visible above rating scales

---

## 4. Block Design

### Structure:
The experiment consists of **2 blocks**, each with different rating questions.

### Participant Group Assignment:
Participants are randomly assigned to one of five participant groups (1, 2, 3, 4, or 5) at the start of the experiment. This determines which subset of candidates they will see.

### Trial Type Assignment:
Participants are randomly assigned to one of three trial type conditions (trial_type1, trial_type2, or trial_type3) at the start of the experiment. This assignment determines which stimuli are presented as photo/bio/dual trials throughout both blocks. These assignments are tracked in the `assigned_group` and `assigned_trial_type` variables in the data.

### Block Questions:

**Block 1: Congressional Competence**
- Familiarity Question: "Before participating, how familiar were you with this person?"
  - Response Options: 
    - "I do not know anything about this person" (coded as 0)
    - "I know who this person is or have heard about them" (coded as 1)
  - **Important**: Candidates marked as familiar (value = 1) are excluded from Block 2
- Primary Question: "How good do you think this person would be as a member of congress?"
  - Scale: 1 (Not at all) to 7 (Very much)
- Confidence Question: "How confident are you in your judgment?"
  - Scale: 1 (Not at all) to 7 (Very much)

**Block 2: Voting Intention**
- Primary Question: "In general, how likely would you be to vote for this person as a U.S. House Representative?"
  - Scale: 1 (Not at all) to 7 (Very much)
- **Stimuli Filter**: Only candidates marked as unfamiliar in Block 1 are shown in Block 2

### Trial Types per Block:
The exact number and distribution of trial types depends on the participant's assigned condition and the materials.csv file. Typically includes:
- **Photo trials**: Only candidate photograph
- **Bio trials**: Only biographical text
- **Dual trials**: Both photograph and biographical text

### Trial Order:
Within each block:
1. Trials are grouped by type (photo, bio, dual)
2. Each group is shuffled randomly
3. The order of the three groups is randomized
4. This creates a random sequence while maintaining type clustering

### Attention Checks:
- **Frequency**: 10% of trials per block (at least 1), randomly positioned
- **Format**: "To ensure you are paying attention, please press the number X on your keyboard."
- **Keys**: Random number between 1-7
- **Feedback**: If incorrect, displays "Wrong answer! Please pay attention to the task." for 2 seconds (centered on screen)
- **No Feedback**: If correct, experiment continues immediately

### Memory Checks:
- **Frequency**: 10% of bio and dual trials per block (rounded up)
- **Timing**: Appears immediately after viewing a bio or dual trial
- **Format**: Yes/No button question based on biographical content (e.g., "Did this person serve in the military?")
- **Response Method**: Click buttons (Yes/No)
- **Time Limit**: 10 seconds to respond
- **Tracking**: Each stimulus can only be used once per block for memory checks
- **Feedback**: 
  - Wrong answer: "Wrong answer! Please pay attention to the biography content." (2 seconds)
  - Timed out: "Too slow! Please respond faster to memory check questions." (2 seconds)
  - Correct: No feedback, continues immediately

### Free Writing Component:
- **Timing**: Appears at the end of each block, before the break/final screen
- **Selection**: One candidate is randomly selected from each trial type (photo, bio, dual) that the participant rated in that block
- **Format**: For each selected candidate, participants see:
  - The candidate's photo (if applicable to trial type)
  - Their rating response displayed
  - A free-response text area
- **Prompt**: "Please briefly explain the reasoning behind your judgment."
- **Submission**: Participants click "Continue" button to proceed to next candidate
- **Purpose**: Collects qualitative data about participants' decision-making process

### Breaks:
- Short break screen appears between blocks (after Block 1 free writing)
- Message: "You have completed block 1 of 2. Take a short break if needed."
- Participants press spacebar to continue

---

## 5. Instructions, Questions, Scales, and Response Method

### Instructions:
Participants see 3 instruction pages before starting:

**Page 1: Welcome and Setup Requirements**
```
Welcome to the Social Impression Rating Task

In this experiment, you will see photos and/or biographies of candidate in the election 
for the U.S. House of Representatives.

Your task is to rate your impression of each person on different dimensions.

Before you begin, please ensure:
• You are in a quiet space where you can focus without distractions
• You are using a computer (not a mobile device or tablet)
• You are using a compatible browser (Chrome, Safari, Firefox, or Edge recommended)

If you have any questions, please contact the researcher at psych-yeslab.study@ucsb.edu.

Press the Next button to continue.
```

**Page 2: Task Structure**
```
Task Structure

The task consists of 2 blocks, each with different questions.

In each block, you will see multiple political candidates and rate them on multiple questions.

There are three types of trials:
• Photo trials: You will make judgments based solely on their profile photos
• Bio trials: You will make judgments based solely on their biographies
• Dual trials: You will make judgments based on both their photos and biographies

Press the Next button to continue.
```

**Page 3: How to Respond**
```
How to Respond

After viewing the photo and/or biography for an amount of time, the rating scale will appear at 
the bottom of the screen.

You will see "Now you can respond" in the top left corner when you can start answering.

To enter your responses:
• For familiarity, click on the button that matches your answer. You can change your answer by 
  clicking a different button.
• For other ratings, use your mouse or trackpad to move the sliders to indicate your ratings
• You can adjust your ratings before submitting
• Press SPACEBAR to submit your answers

Important: Please do your best to make quick and legitimate responses, or you will see a warning.

There will be occasional attention check questions and memory check questions - please read 
carefully!

At the end of each block, you will be asked to briefly explain your judgment for a few randomly 
selected candidates.

Press the Next button to begin.
```

### Eligibility Check:

Before the main experiment begins, participants are asked:

**Question:** "At present, do you have the legal right to vote in the U.S.?"

**Response Options:**
- Yes (allows participant to continue)
- No (ends experiment with message: "Thank you for your interest. This study is only open to individuals who currently have the legal right to vote in the U.S.")

**Data Collected:**
- **task**: "eligibility_check"
- **eligible**: participant's response ("yes" or "no")
- **voting_eligible**: boolean (true if "yes", false if "no")

Only participants who answer "Yes" proceed to the main experiment.

### Block Instructions:

**Block 1:**
```
Block 1 of 2

For this block, you will answer the following questions:

1. Familiarity: Before participating, how familiar were you with this person?

2. How good do you think this person would be as a member of congress?

3. How confident are you in your judgment?

Press the spacebar to begin.
```

**Block 2:**
```
Block 2 of 2

For this block, you will answer the following question:

In general, how likely would you be to vote for this person as a U.S. House Representative?

Press the spacebar to begin.
```

### Rating Questions:

**Block 1 - Congressional Competence:**
- Familiarity Question: "Before participating, how familiar were you with this person?"
  - Button Options: "I do not know anything about this person" | "I know who this person is or have heard about them"
- Primary Question: "How good do you think this person would be as a member of congress?"
- Confidence Question: "How confident are you in your judgment?"

**Block 2 - Voting Intention:**
- Primary Question: "In general, how likely would you be to vote for this person as a U.S. House Representative?"

### Response Scales:

**Familiarity Question (Block 1 only):**
- Type: Binary button choice
- Options:
  - "I do not know anything about this person" (coded as 0)
  - "I know who this person is or have heard about them" (coded as 1)
- Visual feedback: Selected button highlighted in green
- Required: Must click a button before submitting

**All Rating Questions (Competence, Confidence, Vote):**
- Type: 7-point slider scale
- Range: 1 to 7
- Labels:
  - Left anchor (1): "Not at all"
  - Right anchor (7): "Very much"
- Default position: 4 (middle)
- Visual feedback: Numeric value displayed next to slider (changes in real-time)
- Slider appearance: Green circular thumb on gray track

### Response Method:

1. **View Stimulus**: Participant views candidate information for the specified duration (2s for photos, 10s for bios/dual)
2. **Rating Phase Begins**: 
   - Stimulus remains visible at top of screen
   - "Now you can respond" indicator appears in top left corner
   - Rating scales appear below stimulus
3. **Enter Responses**: 
   - For familiarity (Block 1): Click one of two buttons
   - For ratings: Use mouse/trackpad to move sliders
   - Current value (1-7) displays in real-time next to each slider
   - Can adjust multiple times before submitting
4. **Submit Response**: Press SPACEBAR to record ratings and advance to next trial
5. **Submission Prompt**: Text displays "Press SPACEBAR to submit your answers"

### Trial Sequence:
```
Fixation Cross (500ms)
    ↓
Stimulus Presentation (2s for photo, 10s for bio/dual)
    ↓
Rating Phase (stimulus + "Now you can respond" + scales visible)
    ↓
Participant enters responses and presses SPACEBAR
    ↓
[Possible Memory Check for bio/dual trials]
    ↓
[Possible Attention Check]
    ↓
Next trial begins
```

### Overall Experiment Flow:
```
Welcome Screen
    ↓
Eligibility Check
    ↓
[If ineligible: End experiment]
    ↓
Instructions (3 pages)
    ↓
Block 1 Instructions
    ↓
Block 1 Trials (with attention & memory checks)
    ↓
Block 1 Free Writing (3 candidates)
    ↓
Break Screen
    ↓
Block 2 Instructions
    ↓
Block 2 Trials (with attention & memory checks)
    ↓
Block 2 Free Writing (3 candidates)
    ↓
Data Saving & SONA Redirect (if applicable)
```

---

## Data Collection

### Participant Identification:
- **participant_id**: Unique identifier generated at experiment start (format: P[timestamp]_[random string])
- **assigned_group**: Participant group (1, 2, 3, 4, or 5) assigned to participant
- **assigned_trial_type**: Trial type condition (1, 2, or 3) assigned to participant
- **experiment_version**: Version number of the experiment (currently 29)
- **experiment_start_time**: Timestamp when experiment started
- **sona_survey_code**: SONA survey code from URL parameter (or 'NO_SONA_CODE')

### Collected Variables for Rating Trials:
- **task**: "rating"
- **stimulus_name**: Candidate's name (formatted with underscores, e.g., "Adam_Frisch")
- **stimulus_trial_type**: photo, bio, or dual
- **block**: 1 or 2
- **question**: Text of the main rating question
- **competence_response**: Main rating (1-7) for Block 1; null for Block 2
- **vote_response**: Main rating (1-7) for Block 2; null for Block 1
- **familiarity_response**: Familiarity response (0 or 1, Block 1 only; null for Block 2)
  - 0 = "I do not know anything about this person"
  - 1 = "I know who this person is or have heard about them"
- **confidence_response**: Confidence rating (1-7) for Block 1 only; null for Block 2
- **reaction_time_ms**: Reaction time (milliseconds) for response submission
- **response_time_limit_ms**: Time limit allowed for this trial type
- **responded_on_time**: Boolean indicating if response was within time limit
- Standard jsPsych metadata (trial_index, time_elapsed, rt, etc.)

### Collected Variables for Attention Checks:
- **task**: "attention_check"
- **attention_check_question**: Text of the attention check instruction
- **attention_check_correct_key**: The number key that was requested (1-7)
- **attention_check_response**: The key the participant pressed
- **block**: 1 or 2
- **rt**: Reaction time (milliseconds)

### Collected Variables for Memory Checks:
- **task**: "memory_check"
- **stimulus_name**: Candidate's name for the memory check
- **memory_check_question**: Text of the memory question (e.g., "Did this person serve in the military?")
- **memory_check_correct_answer**: Correct answer (0 for No, 1 for Yes)
- **memory_check_response**: Participant's response (0 for No, 1 for Yes, null if timed out)
- **memory_check_correct**: Boolean indicating if response was correct
- **timed_out**: Boolean indicating if participant did not respond in time
- **block**: 1 or 2
- **rt**: Reaction time (milliseconds)

### Collected Variables for Free Writing Trials:
- **task**: "free_writing"
- **stimulus_name**: Candidate's name
- **stimulus_trial_type**: photo, bio, or dual (the trial type of the original rating)
- **block**: 1 or 2
- **rating_given**: The original rating value (competence for Block 1, vote for Block 2)
- **free_response**: Participant's text explanation
- **rt**: Time spent on free writing response (milliseconds)

### Data Storage:
- **Primary**: Automatically sent to PHP backend (save_data.php)
  - Method: POST request with JSON data
  - Response: JSON with success status, filename, and row count
  - On success: Redirects to SONA for credit (if survey code provided) or shows completion message
  - On error: Attempts to redirect to SONA anyway with warning, or shows error message
- **Server Storage**: CSV file saved on server in data/ directory
  - Filename format: `participant_[participantID]_[timestamp]_v[version].csv`
  - One file per participant with all trial data

### SONA Integration:
- **Survey Code**: Extracted from URL parameter `?id=XXXXXX`
  - If present: Stored as `sona_survey_code` in all data rows
  - If absent: Stored as 'NO_SONA_CODE'
- **Completion URL**: https://ucsb.sona-systems.com/webstudy_credit.aspx?experiment_id=4708&credit_token=3f94872037f940acbbe8bb7a6325cd81&survey_code=
  - Survey code automatically appended from URL parameter
- **Redirect Behavior**:
  - On successful data save: Shows alert "Thank you for completing the experiment! You will now be redirected to SONA to receive credit." then redirects
  - On data save error: Offers option to continue to SONA anyway with warning
  - No SONA code present: Shows completion message without redirect

---

## Technical Specifications

### Software:
- jsPsych version 7.3.4
- Plugins: 
  - html-keyboard-response (v1.1.3)
  - image-keyboard-response (v1.1.3)
  - preload (v1.1.3)
  - instructions (v1.1.4)

### Browser Requirements:
- Modern web browser (Chrome, Safari, Firefox, or Edge recommended)
- JavaScript enabled
- Must be accessed via computer (not mobile device or tablet)

### Data Loading:
- Materials loaded from `materials.csv` file
- Bio texts loaded from `bio/` directory
- Images preloaded before experiment begins
- Participant group assignment filters stimuli by `participant_group` column in CSV
- Trial type assignment based on `trial_type1`, `trial_type2`, or `trial_type3` columns in CSV

### Test Mode:
The experiment includes a TEST_MODE constant that can be enabled for faster testing:
- **When enabled** (TEST_MODE = true):
  - Stimulus presentation time reduced to 0ms (instant display)
  - Number of candidates limited to 5 random selections
  - All other functionality remains the same
- **When disabled** (TEST_MODE = false):
  - Normal presentation times (2s for photos, 10s for bio/dual)
  - All candidates from materials.csv are used
  - Production-ready settings
- **Current setting in code**: TEST_MODE = true (should be set to false for actual data collection)

---

## Experiment Duration

### Estimated Time:
- **Eligibility check**: ~5 seconds
- **Instructions**: ~1-2 minutes (3 pages)
- **Per trial**: 
  - Photo trials: ~5-25 seconds (2s presentation + up to 20s response)
  - Bio/Dual trials: ~15-130 seconds (10s presentation + up to 120s response)
- **Memory checks**: ~2-12 seconds (10s time limit + possible 2s feedback)
- **Attention checks**: ~2-5 seconds (response + possible 2s feedback)
- **Free writing** (per candidate): ~30-120 seconds (typically 3 candidates per block)
- **Per block**: Varies based on number and types of trials assigned to participant
- **Break between blocks**: ~10-30 seconds
- **Total experiment**: ~20-50 minutes (including instructions, breaks, and variation based on trial types)

Note: Actual duration depends on:
- Participant's assigned group (determines how many stimuli)
- Participant's assigned trial type condition
- Number of stimuli in materials.csv
- Number of candidates marked as familiar in Block 1 (affects Block 2 length)
- Response speed
- Time spent on free writing responses

---

## Document Version
- **Created**: November 11, 2025
- **Last Updated**: February 18, 2026
- **Experiment Version**: 29
