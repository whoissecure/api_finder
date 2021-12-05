# API Finder
## How to use
```bash
$ python3 api_finder.py -h
usage: api_finder.py [-h] -f FILE -j JSON [-o OUTPUT] -t THREADS

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  File with URLs to inspect.
  -j JSON, --json JSON  Regex file in json format
  -o OUTPUT, --output OUTPUT
                        File to write the output.
  -t THREADS, --threads THREADS
                        Number of threads to use
```
The output file is a optional argument.

## Json format
```json
"Example service": {
    "regex": "[0-9]{12}-[0-9]{12}",
	"links": {
		"0": {
			"link": "https://example.com/api/users?token=APIKEYHERE",
			"method": "get",
			"error": "invalid API key"
		}
	}
},
```
The json file must store the name of the service, the regex of the API key, and the items to test their validity: link(where APIKEYHERE will be replaced with the matched API key), method, post data if its method is POST and error when API key is invalid.

## Example of function to add the script to autorecon script
```bash
apis_scan(){
	if [[ -f $domain/apis/apis.txt ]]; then
		python3 $tool/api_finder.py -f $domain/recon/endpoints/results/endpoints.txt -j $tool/apis.json -t 50 | anew $domain/apis/apis.txt | notify -silent
	else
		python3 $tool/api_finder.py -f $domain/recon/endpoints/results/endpoints.txt -j $tool/apis.json -t 50 -o $domain/apis/apis.txt
		cat $domain/apis/apis.txt | notify -silent
	fi
}
```
With this function I have added the tool to my autorecon script for bug bounty. The function will check if the outfile exists and if it does, it notify only the new lines, otherwise, it use the -o argument and it notifies all the lines.

This implementation needs:
* [notify](https://github.com/projectdiscovery/notify)
* [anew](https://github.com/tomnomnom/anew)

## To do
* Add more services to the example json file.
* Support the addition of headers in the validation of the API key.

## Donations
If you receive a bounty ever with the tool and want to make some donation, you can send some BTC here:
17wL4sZkbFnQN6aNj6eP73e5DUHJFtpWkD

## Credits
I took the links to test the API keys from [keyhacks](https://github.com/streaak/keyhacks).