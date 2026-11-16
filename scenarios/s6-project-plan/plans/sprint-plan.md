# CampusRoute v2.0 "Accessible Campus" - 4-Week Sprint Plan

## 1. Weekly Phases and Goals

- **Week 1 (1–5 March 2027): Foundation & Architecture**  
  *Goal:* Establish data models for step-free routing, opening hours parser, and UI internationalization architecture.
- **Week 2 (8–12 March 2027): Core Feature Implementation**  
  *Goal:* Implement backend endpoints, graph updates (elevators/ramps), and Turkish translation strings while accommodating Ada's exam period.
- **Week 3 (15–19 March 2027): Integration, Badges & Accessibility Testing**  
  *Goal:* Integrate "Open now" badges and Turkish UI toggles into the frontend, and conduct initial 5-persona usability testing.
- **Week 4 (22–26 March 2027): Hardening, Documentation & Code Freeze**  
  *Goal:* Complete regression testing, write bilingual user guides, achieve code freeze by Thu 25 March 18:00, and present live demo on Fri 26 March 14:00.

---

## 2. Team Capacity Analysis

*Note:* Each member attends the 1-hour weekly team sync on Wednesdays. Net task capacity subtracts this 1 hour per week.

| Person | Weekly Total (W1/W2/W3/W4) | Net Weekly Task Capacity (W1 / W2 / W3 / W4) | Total Task Capacity | Strengths & Role |
|---|---|---|---|---|
| **Ada Yilmaz** | 12 / 6 / 12 / 12 h | 11 / 5 / 11 / 11 h | 38 h | Python backend, test harnesses, code review lead |
| **Kerem Demir** | 10 / 10 / 10 / 10 h | 9 / 9 / 9 / 9 h | 36 h | Dijkstra & graph extensions, campus data modeling |
| **Elif Kaya** | 8 / 8 / 8 / 8 h | 7 / 7 / 7 / 7 h | 28 h | Usability testing (5 personas), accessibility UX, docs |
| **Mert Arslan** | 8 / 14 / 14 / 8 h | 7 / 13 / 13 / 7 h | 40 h | Web frontend (JS/CSS), i18n switcher, badge UI |
| **Weekly Total** | **38 / 38 / 44 / 38 h** | **34 / 34 / 40 / 34 h** | **142 h** | — |

---

## 3. Baseline Task Allocation Table

*Must-Ship Backlog Items:* CR-11 (Open now), CR-13 (Step-free v2), CR-19 (Turkish UI).  
*Out of Scope:* CR-14 (POST crowd submissions - omitted per brief).

| Task Description | Backlog ID | Week | Owner | Reviewer | Planned Hours |
|---|---|:---:|---|---|:---:|
| **CR-11** Core `is_open(hours, now)` parser + unit test suite | CR-11 | W1 | Ada | Kerem | 6 h |
| **CR-13** Campus graph schema update: elevator & ramp edge definitions | CR-13 | W1 | Kerem | Ada | 6 h |
| **CR-19** i18n dictionary architecture & key extraction in web UI | CR-19 | W1 | Mert | Elif | 5 h |
| **CR-19** Turkish copy drafting & terminology review | CR-19 | W1 | Elif | Mert | 4 h |
| **Quality** Initial sprint CI setup & test harness verification | Process | W1 | Ada | Kerem | 5 h |
| **CR-13** Dijkstra algorithm update to route through ramps/elevators | CR-13 | W1-W2 | Kerem | Ada | 6 h (3h W1 + 3h W2) |
| **CR-11** API integration: add `open_now` to `/api/places` payload | CR-11 | W2 | Ada | Kerem | 5 h |
| **CR-13** Add synthetic ramp and elevator data to `campus.json` | CR-13 | W2 | Kerem | Elif | 6 h |
| **CR-19** Frontend language toggle button & text switching logic | CR-19 | W2 | Mert | Elif | 7 h |
| **CR-11** Frontend "Open now" / "Closed" pill badges on place cards | CR-11 | W2 | Mert | Ada | 6 h |
| **UX** Usability test plan & 5 persona profiles (including 2 mobility) | UX | W2 | Elif | Mert | 7 h |
| **CR-13** Verification of step-free routes avoiding stair-only paths | CR-13 | W3 | Kerem | Ada | 5 h |
| **CR-19** Turkish search support and diacritic-insensitive keyboard handling | CR-19 | W3 | Mert | Elif | 7 h |
| **CR-11** Dynamic clock selector & schedule-aware opening indicator | CR-11 | W3 | Mert | Ada | 6 h |
| **UX** Run usability sessions with 5 personas; produce findings report | UX | W3 | Elif | Ada | 7 h |
| **Quality** End-to-end integration tests & edge-case test expansions | Process | W3 | Ada | Kerem | 7 h |
| **CR-15** Nice-to-have: CSS Dark Theme support | CR-15 | W3 | Ada | Mert | 4 h |
| **Docs** Bilingual (EN / TR) one-page user guide and documentation | Docs | W4 | Elif | Mert | 7 h |
| **Demo** Presentation rehearsal, demo script & slide deck preparation | Process | W4 | Kerem | Elif | 5 h |
| **Quality** Final regression testing & bug fixing (pre-freeze) | Process | W4 | Ada | Kerem | 7 h |
| **Quality** Accessibility verification (WCAG 2.1 AA screen reader audit) | UX | W4 | Mert | Elif | 5 h |
| **Process** Code freeze checklist & delivery handoff (Thu 25 Mar 18:00) | Process | W4 | Ada | All | 4 h |
| **Process** Live demo preparation (Fri 26 Mar 14:00) | Process | W4 | Kerem | All | 4 h |
| **Process** UI polish & responsive adjustments | Process | W4 | Mert | Elif | 2 h |

---

## 4. Planned vs Available Task Capacity Audit

| Member | W1 Plan / Cap | W2 Plan / Cap | W3 Plan / Cap | W4 Plan / Cap | Total Plan / Cap |
|---|:---:|:---:|:---:|:---:|:---:|
| **Ada** | 11 / 11 h | 5 / 5 h | 11 / 11 h | 11 / 11 h | 38 / 38 h |
| **Kerem** | 9 / 9 h | 9 / 9 h | 5 / 9 h | 9 / 9 h | 32 / 36 h |
| **Elif** | 4 / 7 h | 7 / 7 h | 7 / 7 h | 7 / 7 h | 25 / 28 h |
| **Mert** | 5 / 7 h | 13 / 13 h | 13 / 13 h | 7 / 7 h | 38 / 40 h |
| **Total** | **29 / 34 h** | **34 / 34 h** | **36 / 40 h** | **34 / 34 h** | **133 / 142 h** |

*Audit Verification:* No team member ever exceeds their weekly net task limit. All mandatory PR reviews have an assigned non-author reviewer.

---

## 5. Timeline (Mermaid Gantt Chart)

```mermaid
gantt
    title CampusRoute v2.0 Sprint Timeline
    dateFormat YYYY-MM-DD
    axisFormat %d %b

    section CR-11 Open Now
    Hours parser & tests (Ada)           :a1, 2027-03-01, 2027-03-05
    API open_now integration (Ada)       :a2, 2027-03-08, 2027-03-12
    Frontend badge UI (Mert)             :a3, 2027-03-10, 2027-03-15
    Clock simulation controls (Mert)     :a4, 2027-03-16, 2027-03-19

    section CR-13 Step-Free v2
    Graph schema ramps & elevators (Kerem):k1, 2027-03-01, 2027-03-05
    Dijkstra routing logic (Kerem)       :k2, 2027-03-05, 2027-03-10
    Synthetic campus data enrichment (Kerem):k3, 2027-03-10, 2027-03-12
    Route validation & tests (Kerem)     :k4, 2027-03-15, 2027-03-17

    section CR-19 Turkish UI
    Translation keys & architecture (Mert):m1, 2027-03-02, 2027-03-05
    Turkish copy drafting (Elif)         :e1, 2027-03-03, 2027-03-05
    Language switcher toggle (Mert)      :m2, 2027-03-08, 2027-03-12
    Turkish diacritics & search (Mert)   :m3, 2027-03-15, 2027-03-18

    section Usability & Docs
    Test plan & 5 personas (Elif)        :e2, 2027-03-08, 2027-03-12
    Usability evaluation sessions (Elif) :e3, 2027-03-15, 2027-03-19
    Bilingual user guide EN/TR (Elif)    :e4, 2027-03-22, 2027-03-24

    section Milestones & Release
    Code Freeze (Thu 18:00)              :milestone, m_freeze, 2027-03-25, 0d
    Live Demo & Hand-in (Fri 14:00)      :milestone, m_demo, 2027-03-26, 0d
```

---

## 6. Contingency Re-plan (Change Request: Mert Sick in W3)

### Scenario
In Week 3, Mert falls ill and his available capacity drops from 14 hours to 4 hours (leaving **3 net task hours**).

### Re-plan Adjustments
1. **Drop Nice-to-Have CR-15 (Dark theme):** Frees 4 hours of Ada's time in W3.
2. **Move Frontend UI work to Elif and Ada:**
   - Elif takes on the simpler frontend language toggle styling in W3 (3 h, giving Elif programming practice as requested).
   - Ada implements the frontend badge integration in W3 (4 h) using the time freed from dropping CR-15.
   - Mert focuses only on the essential Turkish diacritic search fix (3 h) during W3.
   - Dynamic clock simulation control is scoped down to using the existing query param or deferred.
3. **Week 4 Adjustments:**
   - Mert returns in W4 at full capacity (7 net h) to handle WCAG accessibility checks and final UI touches.
   - Zero changes to the must-ship scope (CR-11, CR-13, CR-19).
   - Code freeze (25 Mar 18:00) and Demo (26 Mar 14:00) remain strictly on schedule.

### Updated W3-W4 Capacity Table Under Change Request

| Member | W3 Re-planned Task Hours | W3 Capacity | W4 Re-planned Task Hours | W4 Capacity | Status |
|---|:---:|:---:|:---:|:---:|:---:|
| **Ada** | 11 h | 11 h | 11 h | 11 h | On target |
| **Kerem** | 7 h | 9 h | 9 h | 9 h | On target |
| **Elif** | 7 h | 7 h | 7 h | 7 h | On target |
| **Mert** | 3 h | 3 h | 7 h | 7 h | Reduced W3 |
| **Total** | **28 h** | **30 h** | **34 h** | **34 h** | All must-ship items delivered |
