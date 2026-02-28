Based on the documents and the data files in your directory, here is a complete breakdown of what this project is about, what the data contains, and what you need to do.

🎬 What is this Project About?
This project is an experimental study on how film editing affects human memory, specifically looking at event boundaries. The core idea is that when we watch a video or experience something, our brain naturally segments the continuous stream of information into events. The experiment aims to test if abruptly interrupting a video right before a natural event boundary affects a person's ability to encode and recognise that event and its details, compared to letting the video play out naturally.

The participants were divided into two groups:

Natural Cut Group (NB): Watched unaltered videos ending at natural points.
Abrupt Cut Group (AB): Watched videos that were abruptly cut 1-5 seconds before a natural boundary.
During the recognition test, participants were shown frames and had to answer if they had seen them before (Target) or not (Lure), while providing a confidence rating.

📂 What is the Data About?
You have a set of files that log the experiment setup and the participants' responses:

BRSM data csv/ (Directory): Contains 171 individual CSV files. Each file represents a single participant's session logging their key presses, response times, and whether their answers were correct during the encoding and recognition phases.

naturalmovies.csv
 & 

abruptmovies.csv
: Detailed lists of all the videos shown to the Natural Cut and Abrupt Cut groups, respectively, including their durations and which ones were specifically repeated to check for "vigilance" (attention).

target_and_lures.csv
: A log mapping the video IDs to the specific frame images used in the recognition test. It details if the image was a "Before Boundary" (BB) frame or an "Event Middle" (EM) frame.
Demographic data.xlsx: Contains background information about the participants (like age, gender, etc.).
📝 What exactly should you do?
Your main goal is to clean this data, calculate specific psychological memory metrics, and perform statistical analyses to answer the research questions. I have outlined a plan to achieve this.

Here are the specific steps you need to follow:

1. Data Cleaning & Exclusion

Drop invalid data: The experiment brief specifically notes that data for the first 13 participants must be excluded due to a data error.
Calculate Vigilance: You need to calculate how long each participant spent in the "encoding phase" (watching the videos). Any participant who took more than 27.05 minutes should be excluded, as they were likely not paying attention.
2. Calculating Memory Metrics For each participant, you need to calculate:

Recognition Memory Index (REC): Their ability to distinguish old frames from completely new ones. (Formula: P("old" | Target) - P("old" | Foil))
Lure Discrimination Index (LDI): Their ability to distinguish near-identical frames (lures) from the actual frames they saw. (Formula: P("similar" | Lure) - P("similar" | Foil))
3. Statistical Analysis & Visualization You will need to compare the performance of the Natural Cut (NB) group vs. the Abrupt Cut (AB) group across several areas:

General Accuracy & Response Times: Did the Natural Cut group answer more accurately and faster?
Boundary frames (BB): Did the Natural Cut group remember the period right before the boundary better than the Abrupt Cut group?
Event-Middle frames (EM): Was there any significant difference in remembering frames from the middle of an event? (The hypothesis assumes there shouldn't be much difference here).
Create Visualizations: Generate graphs (like bar plots and box plots) comparing these groups to include in a final report.