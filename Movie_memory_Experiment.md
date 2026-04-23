# Movie Memory Experiment

## Objective

This experiment investigates how event segmentation during video encoding affects later memory recognition. Specifically, it examines whether abrupt interruptions at event boundaries impair memory for frames occurring shortly before those boundaries, compared to naturally segmented videos.

## Experimental Design

### Data Files

- `abruptmovies.csv`: Details of the abrupt videos like duration, video name, nature of cut, which boundary
- `naturalmovies.csv`: Details of the natural movies watched by one group of subject
- `target_and_lures.csv`: Details of every target and lure presented in the recognition task
- `cleaned_trials.csv`: Recognition performance and RT in each trial (240 trials)
- `cleaned_summary.csv`: Each subjects summary statistics (all trials)

### Stimuli

A set of short videos (1–2 minutes in length) depicting everyday activities (e.g., cooking, cleaning) was used. Using prior data from independent event segmentation task, event boundaries were identified by using agreement across annotators.

Using these boundaries, two versions of each video were created. In the **Natural Cut** condition, videos ended at their original, uninterrupted timelines. In the **Abrupt Cut** condition, videos were subtly interrupted 1–5 seconds before a consensus event boundary and resumed at a point corresponding to the onset of a new event context. To control for duration effects, the lengths of Natural Cut videos were adjusted such that their average duration matched that of the Abrupt Cut videos.

Two separate group of participants, one group for each condition Abrupt (AB) and Natural (NB), viewed these videos during an **encoding phase**. Participants were instructed to watch the videos attentively. To ensure engagement, five videos were repeated as a **vigilance check**, during which participants were required to press the spacebar to skip repeated clips (see abruptmovies.csv and naturalmovies.csv for details).

Following encoding, participants completed a **recognition task**. On each trial, two frames from the same video were presented: one previously seen (target) and one unseen (lure). The similarity between targets and lures was manipulated across three difficulty levels (easy, moderate, and difficult). After selecting a frame, participants provided a confidence rating on a 5-point scale, where 1 indicated **not at all confident** and 5 indicated **very confident**.

The targets were of **two types**: Before boundary frames (BB), and frames that occurred in middle of an event (EM) (that is between two boundaries).

## Research Question of Interest Examples

(You can think of more)

1. **Recognition accuracy and response times**
   
   Participants who viewed Naturally cut videos are expected to show higher recognition accuracy and faster response times (RTs) compared to those who viewed Abruptly cut videos.

2. **Boundary-related memory effects**
   
   Recognition accuracy for pre-boundary frames is predicted to be higher in the Natural Cut group than in the Abrupt Cut group, reflecting preserved event continuity in the natural condition.

3. **Event-middle frames**
   
   Recognition performance for event-middle frames is expected to not differ significantly between the Natural and Abrupt Cut groups, as these frames are less sensitive to boundary manipulations.

## Statistical Metrics

### 1. Vigilance Calculation

Time between `instruction_2.stopped` to `Videos.stopped` was encoding. Since the repeating videos account for 5.6 mins, anyone accounting for more than 27.05 minutes overall during the encoding stage, was not attentive taking into account 25 secs assumed into recognition for each repeated video before being skipped.

### 2. Other Metrics

- **Recognition Memory Index (REC)**: Measures ability to discriminate Targets from Novel items (bias-corrected).
  - Formula: REC = P("old" | Target) − P("old" | Foil)

- **Lure Discrimination Index (LDI)**: Measures mnemonic discrimination (high-fidelity memory).
  - Formula: LDI = P("similar" | Lure) − P("similar" | Foil)

## Type of Variable

- **Resp.corr**: If identification was correct or not for target
- **Resp.rt**: Response time of key press during recognition
- **_NB**: Natural movie group participant
- **_AB**: Abrupt movie group participant
- **Conf_radio.response**: Confidence rating

## Exclusion/Inclusion Criteria

NA (First 13 participants data not available due to data error)

## Experiment Lead Contact

gargi.shukla@research.iiit.ac.in
