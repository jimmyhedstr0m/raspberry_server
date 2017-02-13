# raspberry_server
This project is a simple and modular python server for controlling power switches and IR-devices. The server requires a configuration file to know which devices to manage.

The system currently supports the following devices:
  - Any IR-device
  - Nexa PE3-1500 power switches

### Dependencies
The server uses several libraries to work. 

#### Flask
Install python [Flask] library for easy API routing.

```sh
$ sudo apt-get install python-pip
$ sudo pip install flask
```

#### Pilight
Install [pilight] to support the 433,92 MHz sender in order to control the power switches.

| Installation steps | Link |
| ------ | ------ |
| Install library | [https://manual.pilight.org/en/installation] [pilight] |
| Wiring electronics | [https://manual.pilight.org/en/electronics-wiring] [pilightWiring] |
| Decode remote | [https://wiki.pilight.org/doku.php/preceive] [pilightReceive] |
| Fix SSDP connection issues | [https://manual.pilight.org/en/faq#pf2] [pilightFix]

Sender cable should be connected to **GPIO17**, and receiver to **GPIO18**.

View help for pilight Nexa devices:
```sh
$ pilight-send -p nexa_switch -H
Usage: pilight-send -p nexa_switch [options]
	 -H --help			display this message
	 -V --version			display version
	 -p --protocol=protocol		the protocol that you want to control
	 -S --server=x.x.x.x		connect to server address
	 -P --port=xxxx			connect to server port
	 -C --config			config file
	 -U --uuid=xxx-xx-xx-xx-xxxxxx	UUID

	[nexa_switch]
	 -t --on			send an on signal
	 -f --off			send an off signal
	 -u --unit=unit			control a device with this unit code
	 -i --id=id			control a device with this id
	 -a --all			send command to all devices with this id
	 -l --learn			send multiple streams so switch can learn
```

Start pilight:
```sh
$ sudo service pilight start
```

Turn on first unit:
```sh
$ pilight-send -p nexa_switch -i <uuid> -u 0 -t
```

Turn on second unit:
```sh
$ pilight-send -p nexa_switch -i <uuid> -u 1 -t
```

Turn on third unit:
```sh
$ pilight-send -p nexa_switch -i <uuid> -u 2 -t
```

Turn on all units:
```sh
$ pilight-send -p nexa_switch -i <uuid> -a -t
```

Turn off all units:
```sh
$ pilight-send -p nexa_switch -i <uuid> -a -f
```

The <uuid> is the remote id and most be decoded in advance with ```pilight-receive```

#### Lirc
[Lirc] is the library for sending and receiving IR-signals.

| Installation steps | Link |
| ------ | ------ |
| Install library | [http://alexba.in/blog/2013/01/06/setting-up-lirc-on-the-raspberrypi/] [lircInstall] |
| Wiring electronics | [http://alexba.in/blog/2013/06/08/open-source-universal-remote-parts-and-pictures/] [lircWiring] |
| Decode IR remote | [http://www.ocinside.de/html/modding/linux_ir_irrecord_guide.html] [lircDecode] |
| List of available key names | [http://www.ocinside.de/modding_en/linux_ir_irrecord_list/] [lircCodes]

After installation lirc should be restarted with ```sudo /etc/init.d/lirc restart```. Add a 22 Ohm resistor before the leds in the wiring scheme to prevent them from burning.

Sender cable should be connected to **GPIO22**, and receiver to **GPIO23**.

### Configuration file
config.json
TODO

License
----

MIT

   [flask]: <http://flask.pocoo.org/>
   [pilight]: <https://manual.pilight.org/en/installation>
   [pilightReceive]: <https://wiki.pilight.org/doku.php/preceive>
   [pilightFix]: <https://manual.pilight.org/en/faq#pf2>
   [pilightWiring]: <https://manual.pilight.org/en/electronics-wiring>
   [Lirc]: <http://www.lirc.org/>
   [lircInstall]: <http://alexba.in/blog/2013/01/06/setting-up-lirc-on-the-raspberrypi/>
   [lircCodes]: <http://www.ocinside.de/modding_en/linux_ir_irrecord_list/>
   [lircDecode]: <http://www.ocinside.de/html/modding/linux_ir_irrecord_guide.html>
   [lircWiring]: <http://alexba.in/blog/2013/06/08/open-source-universal-remote-parts-and-pictures/>
