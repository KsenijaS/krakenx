# How-To: automatic configuration on Linux boot

_How to automatically run krakenx and configure the cooler at boot_.

This guide assumes your init system is systemd, since it is now ubiquitous on
most Linux distributions.

## Create a system service that calls krakenx

Systemd _services_ are configured with _unit_ files.  A basic unit file looks
like this:

```
[Unit]
Description=krakenx automatic configuration

[Service]
Type=simple
ExecStart=/usr/bin/env colctl --mode fading --color_count 2 --color0 192,32,64 --color1 64,11,21 --fan_speed "(30, 60), (45, 100)" --pump_speed "(30, 60), (40, 100)"

[Install]
WantedBy=default.target
```

That should be enough for a system service that calls krakenx.  You can
customize the `ExecStart` line with the `colctr` parameters you would like to
use.

This unit file should be saved in a path that follows the pattern
`/etc/systemd/system/<service name>.service`.  For simplicity, we will
assume you have chosen to name your service `krakenx-config`.

## Testing and enabling the service

Before setting the newly created service to automatically start at every boot,
you should try to start it manually and make sure that it works as intended.

```
# systemctl start krakenx-config
```

After starting the service, use `systemctl`, `journalctl` and `colctl` itself to make sure it is working properly.

```
# systemctl status krakenx-config -n 99
# journalctl -u krakenx-config
# colctl -s
```

Once you are satisfied with the results, _enable_ the service to have it start automatically.

```
# systemctl enable krakenx-config
```

## Uninstalling the service

Before uninstalling the service, first _disable_ it.

```
# systemctl disable krakenx-config
```

Then, simply remove its unit file and _reload_.

```
# rm /etc/systemd/system/krakenx-config.service
# systemctl daemon-reload
```

