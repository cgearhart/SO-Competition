from __future__ import division
from StringIO import StringIO
from math import ceil
from gearley_utilities import *
import dateutil
import datetime
import gzip
import urllib2
import json
import time
import numpy as np
import pandas as pd


def get_closed_state(df,file_name="public_leaderboard.csv"):
    base_url = "http://api.stackoverflow.com/1.1/questions/"
    new_columns = pd.DataFrame(index = df.index,columns=["closed_date","closed_reason"])
    post_ids = df["PostId"]
    questions = []
    closed_dates = []
    closed_reasons = []
    
    print "Initiating SO API requests:"
    for idx in xrange(0,int(ceil(len(post_ids)/100)*100),100):
        url = base_url + ';'.join(post_ids.ix[idx:idx+99].apply(str))
        req = urllib2.Request(url,headers={"Accept-Encoding": "gzip"})
        if idx > 0 and int(idx/100) % 20 == 0:
            print "On index {}. {} to go.".format(idx,len(post_ids)-idx)
            time.sleep(5) # Only 30 requests every second
        try:
            response = urllib2.urlopen(req)
            if response.info().get('Content-Encoding') == 'gzip':
                buf = StringIO(response.read())
                f = gzip.GzipFile(fileobj=buf)
                data = json.loads(f.read())
                questions = questions + data['questions']
        except urllib2.HTTPError,msg:
            print "Bad response for index: {}".format(idx)
    
    print "Post processing"
    for q_idx,question in enumerate(questions):
        if "closed_date" in question:
            date_fts = datetime.date.fromtimestamp(int(question["closed_date"]))
            closed_dates.append(dateutil.parser.parse(str(date_fts)))
            closed_reasons.append(question["closed_reason"])
        else:
            closed_dates.append(np.nan)
            closed_reasons.append("open")
        new_columns["closed_date"] = pd.Series(closed_dates)
        new_columns["closed_reason"] = pd.Series(closed_reasons)
    
    df = df.join(new_columns)
    return df


if __name__=="__main__":
    # Data columns
    # PostId, PostCreationDate, OwnerUserId, OwnerCreationDate, ReputationAtPostCreation, OwnerUndeletedAnswerCountAtPostTime, Title, BodyMarkdown, Tag1, Tag2, Tag3, Tag4, Tag5, PostClosedDate, OpenStatus
    
    #data = build_dataframe(file_name="public_leaderboard.csv")
    data = get_dataframe(file_name="public_leaderboard.csv")
    
    data = get_closed_state(data,file_name="public_leaderboard.csv")
    
    data.save(pickle_path("public_leaderboard.csv"))

    print data.columns
