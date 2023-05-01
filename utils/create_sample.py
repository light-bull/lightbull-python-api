#!/usr/bin/env python3

import lightbull

bull = lightbull.Lightbull("http://localhost:8080", "lightbull")

# Get some data
config = bull.config.get()
parts = config["parts"]

# Create show
show = bull.shows.new_show("Test")
print("New show ID: {}".format(show["id"]))

# Create visual: Single color all parts
visual = bull.shows.new_visual(show["id"], "Single color all parts")
group = bull.shows.new_group(visual["id"], parts, "singlecolor")
print("Visual ID (Single color all parts): {}".format(visual["id"]))

# Create visual: Blink all parts
visual = bull.shows.new_visual(show["id"], "Blink all parts")
group = bull.shows.new_group(visual["id"], parts, "blink")
print("Visual ID (Blink all parts): {}".format(visual["id"]))

# Create visual: Stripes all parts
visual = bull.shows.new_visual(show["id"], "Stripes all parts")
group = bull.shows.new_group(visual["id"], parts, "stripes")
print("Visual ID (Stripes all parts): {}".format(visual["id"]))

# Create visual: Rainbow all parts
visual = bull.shows.new_visual(show["id"], "Rainbow all parts")
group = bull.shows.new_group(visual["id"], parts, "rainbow")
print("Visual ID (Rainbow all parts): {}".format(visual["id"]))
