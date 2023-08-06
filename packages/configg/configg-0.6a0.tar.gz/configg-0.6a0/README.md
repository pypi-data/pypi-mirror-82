# Configg
### Introduction
Simple wrapper module for reading/writing config data like a native python dictionary. Multiple backends provide an identical interface to various file formats (change one line to switch between json & xml). 

Data is arranged into sections, and then by key:value pairs (like a traditional .ini file). This arrangement is consistent across all backends and file formats. Keys must be strings, and values must be strings or values (int, float etc).

### Supported Backends
* ini
* xml
* json
* yml (planned)
* sqlite3 (planned)

### Usage
Here is an example ini config file, "myconfig.ini".
```ini
[user]
username = Peter
id = 5531274123

[database]
type = mongodb
ip = 12.34.56.78
```

Example loading myconfig.ini, and manipulating the data.
```python
from configg import Configg, XML_BACKEND, JSON_BACKEND

# Instantiate Configg
cfg = Configg("myconfig.ini")

# Pull data from user section
username = cfg.user["username"]

# Add data to the user section
cfg.user["token"] = "apples"

# Pull data from the database section
db_ip = cfg.database["ip"]

# Add new section, with new data
cfg.add_section("app_settings", {"resolution": "1024x768"})

# Remove section
cfg.remove_section("app_settings")

# Commit local changes to file 
cfg.commit()

# Reload local data from file
cfg.reload()

# Create new xml config
cfg_xml = Configg("myconfig.xml", data_backend=XML_BACKEND)

# Create new xml config
cfg_json = Configg("myconfig.xml", data_backend=JSON_BACKEND)
```
