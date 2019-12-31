# SyncFile Script

## Motivation

I am a paranoid guy, so I am always backing up my data to multiple sources: cloud, local NAS, external hard drive, etc. The proplem is, I have to do the copy-paste my data from one place to another, click OK whenever the overwritten message popup and I am too lazy for that. Therefore I came up with this script.

## Description

The backbone of this script is dirsync module.

The first thing the script doing is looking for the config.txt file locating in the same folder. The config.txt file contains the path of the source and destination folders. If the config.txt does not exist, the script creates it and prompt user to enter the paths.

The script also checks the format of the configuration file before doing the copy-paste.

The script logs the hash value of the source folder, date/time when the script is run into log.txt file.

After that, the script will copy the folder and its children specified in the source path to the destination paths

## Dependency

For this script, I am using the following modules:

* hashlib
* datetime
* dirsync

so make use you have installed those modules. If you have not done that, please use pip to install them

```python
python -m pip install hashlib
```

```python
python -m pip install datetime
```

```python
python -m pip install dirsync
```

## How to run

* Put the script SyncFile.py to the folder you want to copy. If you run the script for the first time, the script will notify that the config file does not exist and it will create one for you.

![config file is created](https://raw.githubusercontent.com/QuangHaiNguyen/SyncFile/master/doc/pictures/config_created.png)

* Modify the source and the target folders.

![config file template](https://raw.githubusercontent.com/QuangHaiNguyen/SyncFile/master/doc/pictures/config_file_template.png)

* Run the script again

![result](https://raw.githubusercontent.com/QuangHaiNguyen/SyncFile/master/doc/pictures/script_info.png)

* You can check log file for additional information

![log_file](https://raw.githubusercontent.com/QuangHaiNguyen/SyncFile/master/doc/pictures/log_file.png)

## Future development

* More detailed information into log file
* A graphical interface instead of a script

## Change log

### Version 1.0

Initial version

## Contact

For any issues, bugs, errors or suggestions please use Issues or write me an email:

hai.nguyen.quang@outlook.com
