<?php
/**
 * Congress Semantic Experiment - Data Saving Backend
 * 
 * This script receives experiment data from the jsPsych experiment,
 * validates it, and saves it to CSV files (one per participant).
 * 
 * Expected request: POST with JSON body containing array of trial data
 */

// Enable error logging (check server logs for debugging)
error_reporting(E_ALL);
ini_set('display_errors', 0); // Don't show errors to client
ini_set('log_errors', 1);
ini_set('error_log', __DIR__ . '/data/error.log');

// CORS headers - adjust if needed for security
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');
header('Content-Type: application/json');

// Handle preflight OPTIONS request
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

// Only accept POST requests
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'error' => 'Method not allowed']);
    exit();
}

// Configuration
define('DATA_DIR', __DIR__ . '/data/');
define('MAX_FILE_SIZE', 10 * 1024 * 1024); // 10MB limit

// Ensure data directory exists and is writable
if (!file_exists(DATA_DIR)) {
    if (!mkdir(DATA_DIR, 0755, true)) {
        error_log('Failed to create data directory: ' . DATA_DIR);
        http_response_code(500);
        echo json_encode(['success' => false, 'error' => 'Server configuration error']);
        exit();
    }
}

if (!is_writable(DATA_DIR)) {
    error_log('Data directory is not writable: ' . DATA_DIR);
    http_response_code(500);
    echo json_encode(['success' => false, 'error' => 'Server configuration error']);
    exit();
}

// Read and validate input
$rawInput = file_get_contents('php://input');

if (empty($rawInput)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => 'No data received']);
    exit();
}

if (strlen($rawInput) > MAX_FILE_SIZE) {
    http_response_code(413);
    echo json_encode(['success' => false, 'error' => 'Data too large']);
    exit();
}

$data = json_decode($rawInput, true);

if (json_last_error() !== JSON_ERROR_NONE) {
    error_log('JSON decode error: ' . json_last_error_msg());
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => 'Invalid JSON data']);
    exit();
}

if (!is_array($data) || empty($data)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => 'Data must be a non-empty array']);
    exit();
}

// Extract participant ID from data
$participantID = null;
$experimentVersion = null;
$startTime = null;

foreach ($data as $row) {
    if (isset($row['participant_id'])) {
        $participantID = $row['participant_id'];
    }
    if (isset($row['experiment_version'])) {
        $experimentVersion = $row['experiment_version'];
    }
    if (isset($row['experiment_start_time'])) {
        $startTime = $row['experiment_start_time'];
    }
    if ($participantID && $experimentVersion && $startTime) {
        break;
    }
}

if (!$participantID) {
    error_log('No participant_id found in data');
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => 'Missing participant_id']);
    exit();
}

// Sanitize participant ID for filename (remove unsafe characters)
$safeParticipantID = preg_replace('/[^a-zA-Z0-9_-]/', '_', $participantID);

// Create filename with timestamp
$timestamp = date('Y-m-d_His');
$filename = sprintf(
    'participant_%s_%s_v%s.csv',
    $safeParticipantID,
    $timestamp,
    $experimentVersion ?? 'unknown'
);
$filepath = DATA_DIR . $filename;

// Determine all possible column headers from the data
$allHeaders = [];
foreach ($data as $row) {
    $allHeaders = array_merge($allHeaders, array_keys($row));
}
$allHeaders = array_unique($allHeaders);

// Define preferred column order (customize as needed)
$preferredOrder = [
    'participant_id',
    'experiment_version',
    'experiment_start_time',
    'assigned_group',
    'assigned_trial_type',
    'sona_survey_code',
    'task',
    'block',
    'stimulus_name',
    'stimulus_trial_type',
    'competence_response',
    'vote_response',
    'familiarity_response',
    'confidence_response',
    'responded_on_time',
    'reaction_time_ms',
    'response_time_limit_ms',
    'attention_check_question',
    'attention_check_correct_key',
    'attention_check_response',
    'memory_check_question',
    'memory_check_correct_answer',
    'memory_check_response',
    'memory_check_correct',
    'free_response',
    'timed_out',
    'rt',
    'time_elapsed',
    'trial_index',
    'trial_type'
];

// Combine preferred order with any additional headers
$orderedHeaders = [];
foreach ($preferredOrder as $header) {
    if (in_array($header, $allHeaders)) {
        $orderedHeaders[] = $header;
    }
}
// Add any remaining headers not in preferred order
foreach ($allHeaders as $header) {
    if (!in_array($header, $orderedHeaders)) {
        $orderedHeaders[] = $header;
    }
}

// Open file for writing
$file = fopen($filepath, 'w');
if ($file === false) {
    error_log('Failed to open file for writing: ' . $filepath);
    http_response_code(500);
    echo json_encode(['success' => false, 'error' => 'Failed to save data']);
    exit();
}

// Write CSV header
fputcsv($file, $orderedHeaders);

// Write data rows
foreach ($data as $row) {
    $orderedRow = [];
    foreach ($orderedHeaders as $header) {
        $orderedRow[] = isset($row[$header]) ? $row[$header] : '';
    }
    fputcsv($file, $orderedRow);
}

fclose($file);

// Log successful save
error_log(sprintf(
    'Successfully saved data for participant %s (%d rows) to %s',
    $participantID,
    count($data),
    $filename
));

// Return success response
http_response_code(200);
echo json_encode([
    'success' => true,
    'message' => 'Data saved successfully',
    'filename' => $filename,
    'rows' => count($data)
]);
