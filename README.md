# WeatherCN
This script will check `weather.com.cn` every 15 minutes with your location and if it is going to rain, the script will speak in chinese that when it is going to rain. The script will wait until the Weather changed. 

## Requirement
0. GPS device (optional)
1. Download [WhereAmI](https://github.com/robmathers/WhereAmI/releases/download/v1.02/whereami-1.02.zip) and put the executable binary file to your path *This is important if you want to use GPS in macOS*
2. mpg123 `sudo apt-get install mpg123` or `brew install mpg123`
2. lxml `pip install lxml`
3. gtts `pip install gtts`
4. urllib3 `pip install urllib3` (maybe you have already installed)

## Usage
### Recommanded
You can use this script in tmux directly
```shell
tmux new -s WeatherCN
python3 main.py
<C-b d>
```
```shell
nohup python3 main.py &
```