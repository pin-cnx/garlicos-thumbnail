# garlicos-thumbnail
Generate the thumbnail by the list of file and make it look like you browsing them.


[![Image generator](https://img.youtube.com/vi/rwKNEyE0mS4/0.jpg)](https://youtube.com/shorts/rwKNEyE0mS4)

### Install
```
pip install Pillow
```
You have to use Skraper(https://www.skraper.net) to download all of image
so the path of image will end up like
```
SDCARD2
  ├─GBA
  └─SFC
    ├─media
    │ ├─box2dfront
    │ │ ├─GameA.png
    │ │ └─GameB.png
    │ ├─screenshot
    │ │ ├─GameA.png
    │ │ └─GameB.png
    │ └─screenshottitle
    │   ├─GameA.png    
    │   └─GameB.png    
    │
    ├─GameA.smc
    └─GameB.smc
```

### Config
Change path in generate.py
```
base_rom_game_path = "/home/pppstudio/RG35XX/SDCARD2/" # change this to root rom path
base_garlic_rom_path = "/home/pppstudio/RG35XX/ROMS/" # change this to garlic's rom
```
Change your /CFW/skin/setting.json
```
  "text-alignment":"center",
  "text-margin":"0",
```
to
```
  "text-alignment":"left",
  "text-margin":"700",
```


### Run
```
./generate.py
```
