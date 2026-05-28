Dobrea Matei-Stefan, 314CA
# <b><u>Creation of dataset</u></b>

### NOAA - National Oceanic and Atmospheric Administration

For the creation of the dataset, we used the API provided by the NOAA. Through it we managed to download around 4300 data points from a single station in North America. The initial plan was to train the AI model on multiple stations and for it to be able to predict the tide in a more general way, but it proved too complicated for the time we allocated to the project, although this could be a way to develop a more robust predictor. For the initial task we envisioned, 180 000 data points were downloaded.

### Parameters used

Initially the model was supposed to use the time of the measurement, the minor, moderate and major flood levels of the station, the longitude and latitude and a derived information from these 2: whether the station was at the Pacific ocean or Atlantic. Unfortunately, due to the downscaling of the scope of the project, some of those parameters were abandoned, but they were replaced with others that were meant to enchance the model. Firstly we added the 5 latest measurements of water level, in order for it to predict the 6th. Apart from that, the model recieves the mean of the last 24 hours (the value around which it can calculate the new value), the standard deviation of the last 24 hours (how fast the tide is changing, to be able to base its guess on that) and the maximum value of the last 24 hours (how high can it guess). Another parameter that improved it was some sine and cosine functions. Their periods match some important cycles that are linked with the tides: the 12 hour tide cycle of the place we considered, the 24 hour day cycle, the ~15 day Spring/Neap cycle and the ~30 day lunar cycle. These were provided because the model needs some time information and the year/month/day/hour inputs could be a bit confusing for it.

### Water level variable findings

The aformentioned sines and cosines weren't chosen like this because of a guess, but because we observed the repetitions on graphs. Down below can be observed the ~15 day Spring/Neap cycle:

<img src="Tide_graph.png">

And on a smaller scale can be observed the 12 hour tide cycle:

<img src="noaanosco-opsobserved-wa.png">
