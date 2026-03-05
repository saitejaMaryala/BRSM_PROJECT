# BRSM Project 2026

# Background

## Zacks et al, 2007

https://pmc.ncbi.nlm.nih.gov/articles/PMC3314399/pdf/nihms363554.pdf

Event segmentation theory proposes that people parse any continuous flow of events into
smaller, discrete units of meaningful events to make sense of it. Main principle of EST is driven
by prediction errors in perceptual systems arise. Our working memory has event models that
guide our perceptual processing. These models are very stable and provide perceptual
consistency across time. Whenever any activity becomes less predictable, our prediction error
increases. Whenever this prediction error increases, an update in the event models is required
to help the prior event model come to a new stable state.
Event segmentation depends on factors like bottom up processing, which involves sensory cues
that change with change in environment or change in movement. It is also affected by top down
processing, which changes along with prior established event schemata as per new goals and
plans. Event boundaries are perceived when this transient change in perceptual system occurs
and leads to prediction error.
Abrupt disruption from external cues are linked to disruption in memory encoding because the
event model fails to be updated. (Boltz, 1992) showed participants a feature film and
advertisement breaks were inserted at either natural event boundaries or at non boundaries.
Commercials that were at event boundary improved later recall, while non boundary
commercials impaired the memory

## Radvansky & Zacks, 2017

https://pmc.ncbi.nlm.nih.gov/articles/PMC5734104/pdf/nihms903261.pdf

Event horizon model is expanded upon EST and describes how event representations are
structured and affect memory. The fourth principle of this model is about Boundary advantage. It
says that event boundaries serve as anchors in LTM. It means that boundaries facilitate
encoding into LTM as the processing that occurs at these boundaries is important for updating
event models. The boundary advantage can be seen as improvement in encoding and recall
during segmentation along with other benefits that suggest that boundaries are the points that
are majorly retained in our memory.
The paper highlights few studies that show that the participants who had less agreement over
event boundaries with other participants, also performed poorer on memory tests. Study by
(Schwan & Garsoffky, 2004) shows that if we delete time segments between an event, then its recall
will be better than when we delete a time segment from the boundary.
Hence, till now we have established that event boundaries play a major role in both working memory
and LTM. But what if this boundary effect is manipulated? So to dive into it, we will shift towards
experimental manipulations for event boundaries.

## Cutting, Brunick, & Candan(2012)

https://d1wqtxts1xzle7.cloudfront.net/55632820/jephpp12-libre.pdf

This study looked at hollywood films spanning a timeline of 1940-2010. They selected total 24
movies, 3 from each decade. 6 participants had to annotate the clips from these movies twice: once
for fine grained and second for coarse grained boundaries. They quantified few physical metrics as
per EST that could trigger prediction error and hence event segmentation: shot dynamics, motion,
luminance and colour, space time and location. They found that the event boundaries were
perceived majorly on the basis of these bottom up perceptual cues rather than goals of the character
or the story.
Film editing introduces abrupt cuts between successive shots which usually involve physical
changes. These abrupt changes serve are necessary for perceptual prediction and force the viewer's
cognitive system to update the event model. These findings are in sync with the basis of EST which
relates segmentation to change in environment. Hence perceptual manipulation would generate
prediction errors and hence, event boundaries.

## Swallow, Zacks & Abram, 2009:

https://pmc.ncbi.nlm.nih.gov/articles/PMC2819197/pdf/nihms171693.pdf

They did three experiments in which participants watched films with everyday activities. They
defined factors: presentation boundary factor which is if a boundary occurred during presentation of
an object or it did not occur, and delay boundary factor which is if the event boundary occurred in the
subsequent five-second delay between the object's disappearance and the memory test. Across all
the experiment, the items present at the time of boundary perception were better encoded. Boundary
objects were recognized better. Across an event boundary, the boundary advantage is seen even
stronger.
If we relate this study to our previous concept of film editing then this paper identifies instances like a
boundary might occur when a film cuts to a shot of actors carrying laundry down the stairs (a change
in activity and location). It aligns with our goal as abrupt cuts trigger the prediction failure amd hence
affect how memory is encoded. Studies like Boltz 1992, that introduce perceptual shifts tell that
these boundaries leave durable memory traces.

# Experiment Brief

The experiment comprised two phases and involved two independent participant groups. First, a
set of 40 short videos was selected from YouTube Shorts. An independent group of annotators
segmented these videos by indicating **coarse-grained event boundaries** via key presses while
viewing the clips. Event boundaries were derived by computing temporal agreement across
annotators.
Using these boundaries, two versions of each video were created. In the **Natural Cut** condition,
videos ended at their original, uninterrupted timelines. In the **Abrupt Cut** condition, videos were
subtly interrupted **1–5 seconds before a consensus event boundary** and resumed at a point
corresponding to the onset of a new event context. To control for duration effects, the lengths of

Natural Cut videos were adjusted such that their average duration matched that of the Abrupt
Cut videos.
Two separate group of participants, one group for each condition Abrupt(AB) and Natural(NB),
viewed these videos during an **encoding phase**. Participants were instructed to watch the
videos attentively. To ensure engagement, five videos were repeated as a **vigilance check** ,
during which participants were required to press the spacebar to skip repeated clips (see
_abruptmovies.csv_ and _naturalmovies.csv_ for details).
Following encoding, participants completed a **recognition task**. On each trial, two frames from
the same video were presented: one previously seen (target) and one unseen (lure). The
similarity between targets and lures was manipulated across three difficulty levels (easy,
moderate, and difficult). After selecting a frame, participants provided a **confidence rating** on a
5-point scale, where 1 indicated _not at all confident_ and 5 indicated _very confident_. The targets
were of two types : Before boundary frames(BB), and frames that occurred in middle of an
event(EM)(that is between two boundaries).

# Research Question of Interest Examples (You can think of more)

### 1. Recognition accuracy and response times

Participants who viewed Naturally cut videos are expected to show higher recognition
accuracy and faster response times (RTs) compared to those who viewed Abruptly cut
videos.

### 2. Boundary-related memory effects

Recognition accuracy for pre-boundary frames is predicted to be higher in the Natural
Cut group than in the Abrupt Cut group, reflecting preserved event continuity in the
natural condition.

### 3. Event-middle frames

Recognition performance for event-middle frames is expected to not differ significantly
between the Natural and Abrupt Cut groups, as these frames are less sensitive to
boundary manipulations.

# Statistical Metrics

1. To calculate vigilance, please use this method:
   Time between (instruction_2.stopped) to (Videos.stopped) was encoding. Since the
   repeating videos account for 5.6 mins, anyone accounting for more than 27.05 minutes
   overall during the encoding stage, was not attentive taking into account 25 secs assumed
   into recognition for each repeated video before being skipped.

2. Other metrics:
   ● Recognition Memory Index (REC): Measures ability to discriminate
   Targets from Novel items (bias-corrected). Formula: REC = 𝑃 ( “old” ∣
   Target ) − 𝑃 ( “old” ∣ Foil ) )
   ● Lure Discrimination Index (LDI): Measures mnemonic discrimination
   (high-fidelity memory). Formula: LDI = 𝑃 ( “similar” ∣ Lure ) − 𝑃 ( “similar”
   ∣ Foil )

# Type of Variable

**Resp.corr:** If identification was correct or not for target
**Resp.rt:** Response time of key press during recognition
**\_NB** : Natural movie group participant
**\_AB** : Abrupt movie group participant
**Conf_radio.response:** Confidence rating
**Exclusion Inclusion Criteria:** NA (First 13 participants data not available due to data error)
**Experiment lead Contact: gargi.shukla@research.iiit.ac.in**
