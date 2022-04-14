#!/usr/bin/python3

import lightbull

bull = lightbull.Lightbull("http://localhost:8080/api", "lightbull")

# Config
config = bull.config()
effect_map = config['effects']

# Create show
show = bull.shows.new_show("Test")

# Update show
bull.shows.update_show(show["id"], favorite=True)

# Add visual
visual = bull.shows.new_visual(show["id"], "Visual name")

# Update visual
bull.shows.update_visual(visual["id"], "New visual name")

# Add other visual and delete it again
other_visual = bull.shows.new_visual(show["id"], "Delete me")
bull.shows.delete_visual(other_visual["id"])

# Add group
group = bull.shows.new_group(visual["id"], ["horn_left"], "singlecolor")

# Change group
bull.shows.update_group(group["id"], parts=["horn_left", "horn_right"])

# Add another group and delete it again
other_group = bull.shows.new_group(visual["id"], ["hole_left"], "singlecolor")
bull.shows.delete_group(other_group["id"])

# update current
bull.shows.update_current(show["id"], visual["id"])

# Show everything
print("# Data")
for show in bull.shows.get_shows():
    fav = ""
    if show["favorite"]:
        fav = "* "
    print(f"{fav}{show['name']} ({show['id']})")

    # visuals
    for visual_id in show["visualIds"]:
        visual = bull.shows.get_visual(visual_id)
        print(f"    {visual['name']} ({visual['id']})")

        # groups
        if visual['groups']:
            for group in visual['groups']:
                effect = effect_map[group['effect']['type']]
                parts = ', '.join(group['parts'])
                print(f"        {effect}: {parts} ({group['id']})")

                # parameters
                for parameter in group['effect']['parameters']:
                    print(f"            {parameter['name']} - {parameter['type']} ({parameter['id']})")
                    print(f"                Cur: {parameter['current']}")
                    print(f"                Def: {parameter['current']}")

print()

# Current
current = bull.shows.get_current()
current_show = bull.shows.get_show(current["showId"])
current_visual = bull.shows.get_visual(current["visualId"])

print("# Currently playing")
print(f"Show: {current_show['name']} ({current_show['id']})")
print(f"Visual: {current_visual['name']} ({current_visual['id']})")


# Cleanup
bull.shows.delete_show(show["id"])
