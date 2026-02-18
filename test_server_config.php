<?php
/**
 * Server Configuration Test Script
 * 
 * Run this script to verify:
 * - PHP version
 * - Directory permissions
 * - File writing capabilities
 * - Error logging setup
 */

echo "<h1>Server Configuration Test</h1>";
echo "<style>body{font-family:Arial,sans-serif;margin:20px;} .ok{color:green;} .error{color:red;} pre{background:#f0f0f0;padding:10px;}</style>";

// 1. Check PHP Version
echo "<h2>1. PHP Version</h2>";
echo "<p>PHP Version: <strong>" . phpversion() . "</strong></p>";
if (version_compare(phpversion(), '7.0.0', '>=')) {
    echo "<p class='ok'>✓ PHP version is sufficient</p>";
} else {
    echo "<p class='error'>✗ PHP version should be 7.0 or higher</p>";
}

// 2. Check data directory
echo "<h2>2. Data Directory</h2>";
$dataDir = __DIR__ . '/data/';
echo "<p>Data directory path: <code>{$dataDir}</code></p>";

if (!file_exists($dataDir)) {
    echo "<p class='error'>✗ Data directory does not exist. Attempting to create...</p>";
    if (mkdir($dataDir, 0755, true)) {
        echo "<p class='ok'>✓ Successfully created data directory</p>";
    } else {
        echo "<p class='error'>✗ Failed to create data directory</p>";
        echo "<p>You may need to create it manually and set permissions.</p>";
    }
} else {
    echo "<p class='ok'>✓ Data directory exists</p>";
}

// 3. Check write permissions
echo "<h2>3. Write Permissions</h2>";
if (is_writable($dataDir)) {
    echo "<p class='ok'>✓ Data directory is writable</p>";
} else {
    echo "<p class='error'>✗ Data directory is NOT writable</p>";
    echo "<p>Run: <code>chmod 755 " . $dataDir . "</code></p>";
}

// 4. Test file writing
echo "<h2>4. File Writing Test</h2>";
$testFile = $dataDir . 'test_' . date('Y-m-d_His') . '.csv';
$testData = "participant_id,experiment_version,task\nTEST001,1.0,test_task\n";

$result = file_put_contents($testFile, $testData);
if ($result !== false) {
    echo "<p class='ok'>✓ Successfully wrote test file: <code>" . basename($testFile) . "</code></p>";
    
    // Try to read it back
    $readData = file_get_contents($testFile);
    if ($readData === $testData) {
        echo "<p class='ok'>✓ Successfully read back test file</p>";
    } else {
        echo "<p class='error'>✗ File content mismatch</p>";
    }
    
    // Clean up
    if (unlink($testFile)) {
        echo "<p class='ok'>✓ Successfully deleted test file</p>";
    } else {
        echo "<p class='error'>✗ Could not delete test file (file remains)</p>";
    }
} else {
    echo "<p class='error'>✗ Failed to write test file</p>";
}

// 5. Check error logging
echo "<h2>5. Error Logging Configuration</h2>";
echo "<p>Display errors: <strong>" . ini_get('display_errors') . "</strong>";
echo " (should be 0 for production)</p>";
echo "<p>Log errors: <strong>" . ini_get('log_errors') . "</strong>";
echo " (should be 1)</p>";
echo "<p>Error log location: <strong>" . ini_get('error_log') . "</strong></p>";

// 6. Test JSON parsing
echo "<h2>6. JSON Support</h2>";
$testJson = '{"test":"value","number":123}';
$parsed = json_decode($testJson, true);
if (json_last_error() === JSON_ERROR_NONE) {
    echo "<p class='ok'>✓ JSON parsing works correctly</p>";
} else {
    echo "<p class='error'>✗ JSON parsing failed: " . json_last_error_msg() . "</p>";
}

// 7. List existing data files
echo "<h2>7. Existing Data Files</h2>";
if (file_exists($dataDir)) {
    $files = array_diff(scandir($dataDir), ['.', '..', '.gitkeep']);
    if (count($files) > 0) {
        echo "<p>Found " . count($files) . " file(s) in data directory:</p>";
        echo "<ul>";
        foreach ($files as $file) {
            $filepath = $dataDir . $file;
            $size = filesize($filepath);
            $date = date('Y-m-d H:i:s', filemtime($filepath));
            echo "<li><code>{$file}</code> ({$size} bytes, modified: {$date})</li>";
        }
        echo "</ul>";
    } else {
        echo "<p>No files in data directory yet.</p>";
    }
}

// Summary
echo "<h2>Summary</h2>";
echo "<p>If all checks passed above, your server is ready to save experiment data!</p>";
echo "<p><strong>Next step:</strong> Use <a href='test_save_data.html'>test_save_data.html</a> to test the full data saving workflow.</p>";
