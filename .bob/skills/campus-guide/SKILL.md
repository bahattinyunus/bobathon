---
name: campus-guide
description: Use when the user asks for campus navigation, routing advice, accessibility/step-free directions, building hours, or schedule lookups on CampusRoute. Generates step-by-step walking instructions, metric distances, walking time estimates, and accessibility alerts.
---

# Campus Guide Skill

Expert campus navigation, accessibility routing, and schedule coordination for university students.

## Capabilities
1. **Shortest Route Planning:** Calculates optimal walking paths using Dijkstra's algorithm across campus buildings, auditoriums, libraries, and dorms.
2. **Accessibility & Step-Free Advice:** Identifies routes with stairs and recommends alternative step-free paths (elevators/ramps) for students with wheelchairs, mobility aids, or heavy gear.
3. **Hours & Open Badges:** Checks building operating hours including late-night shifts and weekend schedules.
4. **Schedule Coordination:** Correlates student schedules with building locations to prevent lecture delays.

## Rules
- Always quote distances in meters and estimated walking times in minutes (using 80 m/min walking speed).
- Highlight whether a route includes stairs.
- For queries involving detours ("via"), compute sequential paths and combine totals.
- When suggesting study locations, consider real-time crowd occupancy.
