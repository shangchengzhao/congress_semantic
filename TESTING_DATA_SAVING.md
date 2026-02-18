# Testing Data Saving on Web Server

This guide explains how to test that your experiment can successfully save data on a web server.

## Prerequisites

Your web server must have:
- **PHP 7.0+** installed and enabled
- **HTTP server** (Apache, Nginx, etc.)
- **Write permissions** on the `data/` directory

## Step-by-Step Testing Process

### Step 1: Upload Files to Server

Upload these files to your web server:
- `experiment.html`
- `save_data.php`
- `test_server_config.php` (testing script)
- `test_save_data.html` (testing script)
- All files in the `bio/` and `image/` directories

### Step 2: Create Data Directory

Make sure the `data/` directory exists and is writable:

```bash
mkdir -p data
chmod 755 data
```

Or if you need broader permissions (depending on your server setup):
```bash
chmod 777 data
```

### Step 3: Test Server Configuration

Visit `test_server_config.php` in your browser:
```
https://your-server.com/path/to/test_server_config.php
```

This will check:
- ✓ PHP version
- ✓ Data directory exists and is writable
- ✓ File writing works
- ✓ JSON parsing works

**All checks should pass.** If any fail, fix the issues before continuing.

### Step 4: Test Data Saving API

Visit `test_save_data.html` in your browser:
```
https://your-server.com/path/to/test_save_data.html
```

Click the **"Test Save Data"** button. You should see:
- ✓ SUCCESS message
- Filename of the saved data file
- Number of rows saved

### Step 5: Verify Data File Was Created

Check the `data/` directory on your server. You should see a new CSV file like:
```
participant_TEST_1234567890_2026-02-18_143522_v1.0.csv
```

Download and open this file to verify:
- CSV headers are correct
- Test data rows are saved
- All expected columns are present

### Step 6: Test Full Experiment

Run through the complete experiment:
```
https://your-server.com/path/to/experiment.html
```

1. Complete the experiment normally
2. Check browser console (F12) for any errors
3. Look for the success message: `"Data saved successfully"`
4. Verify a new data file was created in the `data/` directory

## Common Issues and Solutions

### Issue: "Not Found" or 404 error when accessing test files

**Causes:**
- Test files not uploaded to server yet
- Files uploaded to wrong directory
- Incorrect URL path

**Solutions:**
```bash
# 1. Find where your experiment.html is located on the server
ssh username@yeslab-survey.psych.ucsb.edu
find /home/www -name "experiment.html"

# 2. Navigate to that directory
cd /home/www/apps/yeslab-survey.psych.ucsb.edu/public_html/congress_semantic

# 3. Upload test files to the same directory (from your local machine)
scp test_server_config.php test_save_data.html username@yeslab-survey.psych.ucsb.edu:/home/www/apps/yeslab-survey.psych.ucsb.edu/public_html/congress_semantic/

# 4. Verify files exist
ls -la test_*.php test_*.html
```

### Issue: "Data directory is NOT writable" after chmod 755

**Cause:**
- The web server user (e.g., `www-data`, `apache`, `nobody`) needs write permission
- `chmod 755` only gives write permission to the owner, not to the web server user

**Solutions (try in order):**

**Option 1: Use chmod 777 (easiest, less secure)**
```bash
cd /home/www/apps/yeslab-survey.psych.ucsb.edu/public_html/congress_semantic
chmod 777 data/

# Then refresh the test_server_config.php page in your browser
```

**Option 2: Change ownership to web server user (more secure)**
```bash
# First, find out what user Apache runs as:
ps aux | grep apache
# or
ps aux | grep httpd

# Common web server users: www-data, apache, nobody, _www

# Then change ownership (replace 'www-data' with your web server user):
sudo chown www-data:www-data data/
chmod 755 data/
```

**Option 3: Add web server user to your group**
```bash
# Find your username and the web server user
whoami
ps aux | grep apache | head -1

# Add web server user to your group (ask your server admin if needed)
sudo usermod -a -G yourusername www-data

# Then set group write permission:
chmod 775 data/
```

**After applying the fix:**
1. Refresh `test_server_config.php` in your browser
2. You should see: "✓ Data directory is writable"
3. You should see: "✓ Successfully wrote test file"

### Issue: "Failed to save data" or 500 error

**Causes:**
- Data directory doesn't exist or isn't writable
- PHP doesn't have permission to create files

**Solutions:**
```bash
# Create directory if missing
mkdir -p data

# Set appropriate permissions
chmod 755 data  # or chmod 777 data if needed

# Check web server user (Apache/Nginx)
# Files created by PHP should be owned by the web server user
```

### Issue: "No data received" or 400 error

**Causes:**
- POST data isn't reaching PHP
- CORS blocking the request
- PHP input stream issues

**Solutions:**
- Check browser console for CORS errors
- Verify `save_data.php` has correct CORS headers (already included)
- Make sure you're accessing via HTTP/HTTPS, not `file://`

### Issue: Empty JSON or "Invalid JSON data"

**Causes:**
- Data not properly formatted
- JavaScript errors preventing data collection

**Solutions:**
- Check browser console for JavaScript errors
- Verify jsPsych is collecting data properly
- Use `test_save_data.html` to isolate the save_data.php functionality

### Issue: PHP file downloads instead of executing

**Causes:**
- PHP not enabled or configured on the server
- Wrong file extension or MIME type

**Solutions:**
- Contact your hosting provider to enable PHP
- Ensure `.php` files are configured to execute
- Check Apache/Nginx configuration

## Directory Permissions Guide

### Recommended Permissions

```bash
chmod 755 /path/to/experiment/          # Main directory
chmod 644 /path/to/experiment/*.html    # HTML files
chmod 644 /path/to/experiment/*.php     # PHP files
chmod 755 /path/to/experiment/data/     # Data directory (writable)
chmod 755 /path/to/experiment/bio/      # Bio directory
chmod 755 /path/to/experiment/image/    # Image directory
chmod 644 /path/to/experiment/bio/*     # Bio text files
chmod 644 /path/to/experiment/image/*   # Image files
```

### If chmod 755 doesn't work for data directory

Some servers require `chmod 777` for the web server to write files:
```bash
chmod 777 data
```

**Security note:** Only use 777 if necessary, and only on the data directory.

## Monitoring Data Collection

### Check Data Files Regularly

```bash
# List all data files
ls -lh data/

# Count number of participants
ls data/participant_*.csv | wc -l

# View most recent file
ls -t data/participant_*.csv | head -1
```

### Check Error Logs

If issues occur, check the error log:
```bash
tail -f data/error.log
```

Or your server's PHP error log:
```bash
tail -f /var/log/apache2/error.log    # Apache
tail -f /var/log/nginx/error.log      # Nginx
```

## Production Checklist

Before running with real participants:

- [ ] All test scripts (test_*.php, test_*.html) work correctly
- [ ] Data directory is writable
- [ ] At least one test data file has been successfully saved
- [ ] Test data file contains all expected columns
- [ ] Experiment runs without console errors
- [ ] SONA redirect works (if applicable)
- [ ] Backup plan in place for data directory
- [ ] Regular monitoring scheduled

## Local Testing (Optional)

To test locally before uploading to server:

### Option 1: PHP Built-in Server

```bash
cd /path/to/experiment
php -S localhost:8000
```

Then visit: `http://localhost:8000/test_server_config.php`

### Option 2: MAMP/XAMPP (macOS/Windows)

1. Install MAMP or XAMPP
2. Place experiment files in the `htdocs` directory
3. Start Apache and PHP
4. Visit: `http://localhost/experiment/test_server_config.php`

## Questions?

If you encounter issues not covered here, check:
1. Browser console (F12 → Console tab) for JavaScript errors
2. Network tab (F12 → Network tab) to see the POST request to save_data.php
3. Server PHP error logs
4. File permissions on the data directory
