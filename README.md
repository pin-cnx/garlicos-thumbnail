# garlicos-thumbnail

[![Image generator](https://img.youtube.com/vi/rwKNEyE0mS4/0.jpg)](https://youtube.com/shorts/rwKNEyE0mS4)

### Install
```
pip install Pillow
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
