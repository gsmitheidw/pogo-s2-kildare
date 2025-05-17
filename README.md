# Pokemon Go S2 Mapping Kildare

Draws cells, stops gyms and non-PoGo entities over an OpenStreetView  
Map to aid positioning and co-ordinating.

### Features
- Pulls data from a csv file (not live updates and not relying on IITC/Ingress)
- Simple - only shows a grid for the town area
- Can run static from a local pc/phone, does not require a hosted webserver

## Preview:
![map preview](pogo-kildare.png)


## Building your own copy locally:

- install python & pip
- install justfile
- clone this repo
- run ```just build``` or ```just rebuild```
- open index.html in a browser

