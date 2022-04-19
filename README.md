# Meme De-Fryer
## Where memes are pristenely cleaned  
COVID-19 apocalypse quarantine "passion" project

## Goal
### Original:
![Deep fried meme](img/deepfried.png "Deep fried meme")
### Processed:
![Clean meme](img/unfried.png "Clean meme")
## Progress
### After noise smoothing and desaturation
![Smoothing](img/smoothing.png "Smoothing")

### Notes
**Image padding**
The meme templates are all various sizes, so we need to pad them to the same size for the network
to be able to use them. To decide what size to use, we searched the template files for the largest
height or width and used that as the width of the largest image.
