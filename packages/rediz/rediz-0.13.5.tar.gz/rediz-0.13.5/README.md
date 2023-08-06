

# Rediz 

Server code for open community microprediction at www.microprediction.org.  

### Microprediction.Org 

![](https://i.imgur.com/yKItXmT.png)

### Overview 

The python packages called "microprediction" (user client library) and "rediz" (system implementation using redis as transport) are demonstrated at www.microprediction.org, where they 
make it easy for anyone who needs a live source of data predicted to receive help from clever humans and self-navigating time series algorithms.  They do this by:

 - Obtaining a write_key with microconventions.create_key(difficulty=12), which takes several hours
 - Using the write_key to update a live quantity, such as https://www.microprediction.org/live/cop.json
 - Repeating often.  

They can then access history (e.g. https://www.microprediction.org/live/lagged::cop.json) and predictions (e.g. https://www.microprediction.org/cdf/cop.json). This is an easy way to 
normalize data and perform anomaly detection. Over time it may garner other insights such as assessment of the predictive value of the data stream the identities of streams that
might be causally related. 

This setup is especially well suited to collective prediction of civic data streams such as transport, water, electricity, public supply chain indicators or the spread of infectious diseases. The client 
library 
https://github.com/microprediction/rediz/blob/master/README.md and site www.microprediction.org provide more information. 

### Related packages and dependencies

     muid      getjson
       |           |
     microconventions 
       |           | 
     rediz        microprediction
  

- Conventions https://github.com/microprediction/microconventions/blob/master/README.md
- Microprediction https://github.com/microprediction/rediz/blob/master/README.md

### Rediz details

This may be a little stale. 

 - https://github.com/microprediction/rediz/blob/master/README_REDIZ.md 
 - https://github.com/microprediction/rediz/blob/master/README_REDIZ_DETAILS.md


