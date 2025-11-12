# Congressional Candidate Social Impression Rating Experiment

## Experimental Procedure Documentation

---

## Overview
This experiment measures social impressions of congressional candidates across three dimensions: competence, voting intention, and electability. Participants view candidate information (photos, biographical text, or both) and provide ratings on 7-point scales.

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
The experiment consists of **3 blocks**, each with a different rating question.

### Block Questions:

**Block 1: Competence**
- Question: "How good do you think this person would be as a member of congress?"
- Scale: 1 (Not at all) to 7 (Very much)
- Additional Question: "Except the information you just learned, are you familiar with this person?"
  - Scale: 1 (I don't know this person at all) to 7 (Very familiar)

**Block 2: Voting Intention**
- Question: "In general, how much would you like to vote for this person?"
- Scale: 1 (Not at all) to 7 (Very much)
- No familiarity question

**Block 3: Electability**
- Question: "How likely do you think this person would win the election"
- Scale: 1 (Not at all) to 7 (Very much)
- No familiarity question

### Trial Types per Block:
Each block contains the same stimuli presented in different formats:
- **Photo trials**: Only candidate photograph (3 trials)
- **Bio trials**: Only biographical text (3 trials)
- **Dual trials**: Both photograph and biographical text (3 trials)

### Randomization:
- Stimuli are randomized within each block
- Trial order is different for each participant

### Attention Checks:
- **Frequency**: Randomly inserted at 10% of trials per block
- **Format**: "To ensure you are paying attention, please press the number X on your keyboard."
- **Keys**: Random number between 1-7
- **Feedback**: If incorrect, displays "Wrong answer! Please pay attention to the task." for 2 seconds (centered on screen)
- **No Feedback**: If correct, experiment continues immediately

### Breaks:
- Short break screen appears between blocks
- Message: "You have completed block X of 3. Take a short break if needed."
- Participants press spacebar to continue

---

## 5. Instructions, Questions, Scales, and Response Method

### Instructions:
Participants see 3 instruction pages before starting:

**Page 1: Welcome**
```
Welcome to the Social Impression Study

In this experiment, you will see information about different political candidates.

For each candidate, you will be asked to rate them on different dimensions.

Press the spacebar to continue.
```

**Page 2: Task Structure**
```
Task Structure

The experiment has 3 blocks.

In each block, you will see information about candidates in different formats:
- Photos only
- Biographical information only
- Both photos and biographical information

You will be asked a question and rate each candidate on a scale from 1 to 7.

Press the spacebar to continue.
```

**Page 3: How to Respond**
```
How to Respond

For each candidate:
1. You will see their information briefly
2. Then, you will be asked to rate them using sliders

Use your mouse or trackpad to adjust the sliders.

When you're ready to submit, press the SPACEBAR.

Try to respond as quickly and accurately as possible.

Press the spacebar to begin the experiment.
```

### Rating Questions:

**Block 1 - Competence:**
- Primary Question: "How good do you think this person would be as a member of congress?"
- Familiarity Question: "Except the information you just learned, are you familiar with this person?"

**Block 2 - Voting Intention:**
- Primary Question: "In general, how much would you like to vote for this person?"

**Block 3 - Electability:**
- Primary Question: "How likely do you think this person would win the election"

### Response Scales:

**All Primary Questions:**
- Type: 7-point slider scale
- Range: 1 to 7
- Labels:
  - Left anchor (1): "Not at all"
  - Right anchor (7): "Very much"
- Default position: 4 (middle)
- Visual feedback: Numeric value displayed next to slider

**Familiarity Question (Block 1 only):**
- Type: 7-point slider scale
- Range: 1 to 7
- Labels:
  - Left anchor (1): "I don't know this person at all"
  - Right anchor (7): "Very familiar"
- Default position: 4 (middle)
- Visual feedback: Numeric value displayed next to slider

### Response Method:

1. **View Stimulus**: Participant views candidate information for the specified duration
2. **Rating Phase Begins**: Stimulus remains visible, rating scales appear below
3. **Adjust Sliders**: 
   - Participants use mouse/trackpad to move sliders
   - Current value (1-7) displays in real-time next to each slider
   - Can adjust multiple times before submitting
4. **Submit Response**: Press SPACEBAR to record ratings and advance to next trial
5. **Submission Prompt**: Text displays "Press SPACEBAR to submit your answers"

### Trial Sequence:
```
Fixation Cross (500ms)
    ↓
Stimulus Presentation (2s or 10s depending on trial type)
    ↓
Rating Phase (stimulus + sliders visible)
    ↓
Participant adjusts sliders and presses SPACEBAR
    ↓
Next trial begins
```

---

## Data Collection

### Collected Variables:
- **stimulus_name**: Candidate's name
- **trial_type**: photo, bio, or dual
- **block**: 1, 2, or 3
- **question**: Text of the rating question
- **rating**: Main rating (1-7)
- **familiarity_rating**: Familiarity rating (1-7, Block 1 only; null for Blocks 2-3)
- **rt**: Reaction time (milliseconds)
- **responded_on_time**: Boolean indicating if response was within time limit
- **correct**: For attention checks, whether response was correct
- **phase**: stimulus_presentation or rating
- Standard jsPsych metadata (trial_index, time_elapsed, etc.)

### Data Format:
- CSV file
- Automatically downloads at experiment completion
- Filename format: `congress_semantic_data_[timestamp].csv`

---

## Technical Specifications

### Software:
- jsPsych version 7.3.4
- Plugins: html-keyboard-response, image-keyboard-response, preload, instructions

### Browser Requirements:
- Modern web browser (Chrome, Firefox, Safari, Edge)
- JavaScript enabled
- Local storage enabled

### Hosting:
- Requires web server (cannot run from file:// protocol)
- Test server: Python HTTP server on localhost:5500

---

## Experiment Duration

### Estimated Time:
- **Per trial**: ~5-15 seconds (depending on trial type and response time)
- **Per block**: ~3-5 minutes (9 trials + attention checks)
- **Total experiment**: ~10-20 minutes (including instructions and breaks)

---

## Document Version
- **Created**: November 11, 2025
- **Last Updated**: November 11, 2025
- **Experiment Version**: 1.0
