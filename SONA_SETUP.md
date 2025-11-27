# SONA Integration Setup Guide

This experiment is now integrated with SONA for automatic credit granting.

## How It Works

1. **Survey Code Capture**: The experiment extracts the SONA survey code from the URL parameter `?id=XXXXXX`
2. **Data Recording**: The survey code is saved with all experimental data
3. **Automatic Redirect**: After completing the experiment and saving data, participants are automatically redirected to SONA to receive credit

## Setup Instructions

### Step 1: Get Your SONA Completion URL

1. Log in to your SONA system as a researcher
2. Go to your study settings
3. Find the **Client-Side Completion URL** (not server-side)
4. It should look like this:
   ```
   https://umd.sona-systems.com/webstudy_credit.aspx?experiment_id=XXXX&credit_token=YYYY&survey_code=%SURVEY_CODE%
   ```
   (Replace `umd` with your institution's SONA subdomain)

### Step 2: Update the Experiment Code

1. Open `experiment.html`
2. Find this line (around line 270):
   ```javascript
   const SONA_COMPLETION_URL = 'https://umd.sona-systems.com/webstudy_credit.aspx?experiment_id=XXXX&credit_token=YYYY&survey_code=';
   ```
3. Replace with your actual SONA completion URL, but:
   - Remove the `%SURVEY_CODE%` part at the end
   - Keep the `survey_code=` parameter name
   - Example:
     ```javascript
     const SONA_COMPLETION_URL = 'https://umd.sona-systems.com/webstudy_credit.aspx?experiment_id=1234&credit_token=abcdef123456&survey_code=';
     ```

### Step 3: Configure Your SONA Study

1. In SONA, set up your study as a **"Study URL (Directing participants to an external webpage)"**
2. Set the study URL to:
   ```
   https://shangchengzhao.github.io/congress_semantic/experiment.html?id=%SURVEY_CODE%
   ```
3. SONA will automatically replace `%SURVEY_CODE%` with each participant's unique code

### Step 4: Test the Integration

1. **Test Mode**: Before launching, test with the current `TEST_MODE = true` setting
2. **Get a Test URL**: From SONA, get a test participant link (it will include `?id=XXXXXX`)
3. **Complete the Task**: Go through the entire experiment
4. **Verify**:
   - Data is saved to Google Sheets with the `sona_survey_code` field
   - You are redirected to SONA after completion
   - Credit is granted in SONA

5. **Disable Test Mode**: Once testing is complete, set `TEST_MODE = false` in the code

## How Participants Access the Study

When participants sign up through SONA, they will click a link that looks like:
```
https://shangchengzhao.github.io/congress_semantic/experiment.html?id=100179
```

The experiment will:
1. Extract `100179` as the survey code
2. Save it with all data
3. After completion, redirect to SONA with that code to grant credit

## Error Handling

The integration includes robust error handling:

- **If data save succeeds**: Participant is automatically redirected to SONA
- **If data save fails**: Participant gets a confirmation dialog asking if they want to continue to SONA
- **No SONA code**: If accessed without `?id=` parameter, works as normal experiment without SONA redirect

## Data Fields

The SONA survey code is saved in the data as:
- **Field name**: `sona_survey_code`
- **Example value**: `"100179"` (from URL parameter)
- **No SONA value**: `"NO_SONA_CODE"` (if accessed without the parameter)

## Troubleshooting

### Participants not getting credit
- Verify the `SONA_COMPLETION_URL` is correct
- Check that the experiment_id and credit_token are valid
- Make sure the SONA study URL includes `?id=%SURVEY_CODE%`

### Survey code not appearing in data
- Check the URL includes `?id=` parameter
- Look in browser console for "SONA Survey Code:" log message

### Redirect not happening
- Check browser console for errors
- Verify `SONA_COMPLETION_URL` is properly set
- Make sure the experiment completes without errors

## Important Notes

- The **client-side completion URL** is used (not server-side) because it allows for graceful error handling
- Participants see an alert before being redirected to SONA
- The survey code is logged to the browser console for debugging
- Even if data saving fails, participants can still receive SONA credit (with confirmation)
