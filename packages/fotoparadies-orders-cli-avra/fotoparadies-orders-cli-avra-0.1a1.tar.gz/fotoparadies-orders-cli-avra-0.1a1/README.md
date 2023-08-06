# fotoparadies-orders-cli
Unofficial command line interface for keeping track of dm Fotoparadies orders.

You can use it to store a list of orders (todo) or check your order directly via cli.

It uses the same api your browser would contact when using the website.

## Installation
You can install it from PyPi

```
pip install --user fotoparadies-orders-cli-avra
```

I do not provide the api endpoint. You will need to set this up on your own. If there is an ```api_endpoint.txt``` in the current path the program will load its content as the endpoint. You can also specify the endpoint in your environment variables as ```FOTOPARADIES_API_URL```. If your default shell is bash you can use:

```bash
echo 'export FOTOPARADIES_API_URL=<API_URL>' >> ~/.bash_profile
```

The env variable will be prioritized over ```api_endpoint.txt```.

## Usage

```
usage: -m [-h] [--shop SHOP] [--order ORDER] [--json]
```
```
optional arguments:
  -h, --help            show this help message and exit
  --shop SHOP, -s SHOP  shop number, used for direct api call
  --order ORDER, -o ORDER
                        order number, used for direct api call
  --json                return json of api call if using --shop and --order
```
```bash
$ fotoparadies                    # can be used without args to open a menu

$ fotoparadies -s 000 -o 000000   # returns order state immediately
2020-09-23: DELIVERED
Ihr Auftrag liegt zur Abholung bereit.
2,90 €
```

## Contributing
Pull requests/issues are welcome.

## Disclaimer
This is an unofficial interface. This is in no way affiliated with dm, dm Fotoparadies or any of its subsidiaries. Use at your own risk.

## License
[MIT](https://choosealicense.com/licenses/mit/)