# raspberry_server

# Useful links for setting up pilight and lirc
Wiring lirc: http://alexba.in/blog/2013/06/08/open-source-universal-remote-parts-and-pictures/
Remember to add an 22 ohm resistor before the leds so they don't burn

Connect sender to GPIO22, receiver to GPIO23

Learn lirc remotes: http://www.ocinside.de/html/modding/linux_ir_irrecord_guide.html

Wiring pilight: https://manual.pilight.org/en/electronics-wiring
Connect sender GPIO17, receiver to GPIO18

Pilight Ssdp Error: https://manual.pilight.org/en/faq#pf2

GPIO chart for raspberry pi 3: https://s-media-cache-ak0.pinimg.com/originals/84/46/ec/8446eca5728ebbfa85882e8e16af8507.png

Receive 433mhz signals pilight: https://wiki.pilight.org/doku.php/preceive

Pilight Nexa help:
pilight-send -p nexa_switch -H

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


Turn on first:
pilight-send -p nexa_switch -i <uuid> -u 0 -t

Turn on second:
pilight-send -p nexa_switch -i <uuid> -u 1 -t

Turn on third:
pilight-send -p nexa_switch -i <uuid> -u 2 -t

Turn all on:
pilight-send -p nexa_switch -i <uuid> -a -t

Turn all off:
pilight-send -p nexa_switch -i <uuid> -a -f
