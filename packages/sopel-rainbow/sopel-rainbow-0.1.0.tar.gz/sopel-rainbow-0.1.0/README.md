# sopel-rainbow

A Sopel plugin to make things RAINBOW COLORED.


## Configuration

By default, `sopel-rainbow` outputs colors in the "standard" rainbow `order`,
ROYGBIV, subject to receiving clients' use of the customary meanings for IRC
color codes 0-15. If set explicitly in your Sopel config file, this default
value would look like:

```ini
[rainbow]
order =
    4
    7
    8
    3
    12
    2
    6
```

If you want to get creative (or cater to a community with shared color norms
that differ from the "de facto" values established by mIRC and friends)
override the `order` with your own list of _numeric_ codes:

```ini
[rainbow]
order = # Americans and French can fight over this one
    4
    0
    2
```

Starting the rainbow at the beginning of the `order` every time is also
default behavior. If you want the rainbow to start at a random place every
time instead, set the Boolean option `random_start` to `yes` or `on`:

```ini
[rainbow]
random_start = on
```


## Dependencies

Only Sopel itself, version 7.0 or higher.

If installed on a bot using Sopel 7.1+, `sopel-rainbow` will strip control
codes from the input text before applying the rainbow colors. (Sopel 7.0.x
does not offer this feature, so feeding formatted text into the `.rainbow`
command might yield unexpected results.)

This version of `sopel-rainbow` will not work with Sopel 9.0+. A future
release will correct this, sometime before Sopel 9 becomes stable.
