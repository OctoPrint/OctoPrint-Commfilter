# OctoPrint-Commfilter

The Commfilter plugin is useful in those situations where your workflow somehow
generates lines into your GCODE files you definitely never want to send to your
printer.

Examples for this include data delimiters such as `%` from CNC GCODE,
certain GCODEs known to cause issues with your printer or basically anything
else you can think of.

## Setup

Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

    https://github.com/OctoPrint/OctoPrint-Commfilter/archive/master.zip

## Configuration

``` yaml
plugins:
  commfilter:
    # filtered GCODEs
    gcode:
      queuing:
      - list
      - of
      sending:
      - filtered
      - gcodes

    # filtered regular expression patterns
    regex:
      queuing:
      - some regex pattern
      - some other regex pattern
      sending:
      - yet another regex patter

    # filtered command types
    command_type:
      queuing:
      - some command type
      sending:
      - some other command type
```

## Usage Examples

To filter all `M117` commands (since you do not have a display on your printer
and they would hence not makes sense), enter `M117` into the list of filtered
GCODEs.

To filter lines beginning with `%` before they are even enqueued into the send
queue, define `^%` as a regular expression pattern for the queuing phase, or
to allow queuing (e.g. for further pre processing plugins) but never allow
sending of such lines, define the same pattern for the sending phase.

To filter all SD status commands of command type `sd_status_poll` and by that
suppressing progress reporting for SD printing entirely (why you would want
to do that is however a completely different question), add `sd_status_poll` to the
list of filtered command types.
