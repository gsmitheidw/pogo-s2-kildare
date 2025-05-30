# Pokemon Go S2 Mapping Kildare

Draws cells, stops gyms and non-PoGo entities over an OpenStreetView  
Map to aid positioning and co-ordinating. Click here for the map:  


[Kildare Town Map](https://gsmitheidw.github.io/pogo-s2-kildare/)


### Features
- Pulls data from a csv file (not live updates and not relying on IITC/Ingress)
- Simple - only shows a grid for the town area
- Can run static from a local pc/phone, does not require a hosted webserver
- Tint cells (L17) to indicate if there is more than one point of interest per cell (none/green/orange/red)  
- Will zoom to your current GPS location
- Allows for categories of Points of Interst such as Gyms and PokéStops  
 but also Non-Pokémon Go (Ingres portal), Nominated and Potential
- Can be localised to any town or location (see below)

#### Marker Legends


| Marker Colour | Legend | Purpose   | Notes                                             |
| ------------- | ------ | --------- | ------------------------------------------------- |
| Blue          | 🔵     | PokéStop  | Regular Pokestops                                 |
| Red           | 🔴     | Gym       |                                                   | 
| Grey          | ❔     | Non-PoGo  | Approved nominations that do not show in the game |
| Purple        | 🟣     | Nominated | Items currently in queue or in voting in wayfarer |

**Non-pogo** - this is useful because a cell could be occupied by an item that only exists in Ingres,  
yet only 1 PokéStop can appear per Layer 17 cell. Or it could be that the nomination was approved
but simply was used in other Niantic games.

## Preview:
![map preview](pogo-kildare.png)


## Building your own copy locally:

1. Clone repo and install python & pip

```bash
git clone https://github.com/yourusername/pogo-s2-kildare.git
cd pogo-s2-kildare
# create virtual environment for python:
python3 -m venv venv
source venv/bin/activate   # Or for Windows use path: venv\Scripts\activate
# Asuming pyton pip is already installed via apt or choco or winget etc:
pip install --upgrade pip
pip install -r requirements.txt
```

2. Install "just" command runnner using apt or choco or winget etc - see https://github.com/casey/just
3. Amend your csv file with Points of Interest. This is the example format:

```csv
name,lat,lng,type,notes
Kildare Square,53.157004,-6.910557,Gym,"Centre of the town"
"Leabharlann Cill Dara, Kildare Library",53.156641,-6.912269,PokéStop
"Kildare Derby Legends Trail Marker 8 of 12",53.155120,-6.911573,Nominated
```

It's probably a good idea to put double quotes around notes or anything that has a comma or special characters in the name.  
If there's quotes in the name, use double quotes.


4. Replace the name for your csv file in s2.py replacing ```kildare_poi.csv``` with ```<yourtown>.csv```
5. Set the GPS co-ords for the centre of your town in s2.py:

Change these lines:

```python
center_lat = 53.1586
center_lng = -6.9096
```


6. Run ```just build``` or ```just rebuild``` - also remember ```just validate``` to check the csv file for errors. If you prefer to run manually:

```bash
python3 s2.py
```

This will generate the index.html file. 

7. Open index.html in a browser or host it on a webserver as you see fit. 


## Chart of S2 cells and Gym Trigger Logic:


```mermaid
flowchart TD
    %% === S2 Structure and Limits ===
    subgraph "🧱 S2 Cell Rules"
        A[🟡 L14 Cell<br/>~2.4km²<br/>Used for Gym eligibility logic. <br/>Contains 64 x L17 cells. Can have up to 3 Gyms, depending on the number of unique L17 cells with PokéStops.] --> B[🔵 L17 Cell<br/>~150m²<br/>Only one PokéStop or Gym allowed per L17 cell. This is the primary density limiter for in-game POIs. There are rare exceptions]
        B --> C[🟢 L20 Cell<br/>~12m²<br/>Used for wild spawns<br/>Max 1 spawn point per cell]
    end

    %% === Stop Distribution and L14 Calculation ===
    A --> D[🔍 Count PokéStops in this L14 cell]
    D --> E{📊 How many PokéStops<br/>in distinct L17 cells?}

    E -->|0-1| F[❌ No Gym created]
    E -->|2-5| G[✅ 1 Gym<br/>Top-ranked PokéStop]
    E -->|6-19| H[✅✅ 2 Gyms<br/>Top 2 ranked]
    E -->|20+| I[✅✅✅ 3 Gyms<br/>Top 3 ranked]

    %% === Notes ===
    subgraph "📝 Notes"
        N1[🔵 L17 limits PokéStop/Gym density<br/>Only one per L17 cell]
        N2[🟡 L14 determines gym conversion rules<br/>Up to 3 gyms per cell]
        N3[🟢 L20 governs wild Pokémon spawn eligibility<br/>Usually 1 spawn per cell; not all L20s used]
        N4[⭐ Top-ranked = Niantic's internal POI score<br/>Based on edits, scans, popularity]
    end
```

