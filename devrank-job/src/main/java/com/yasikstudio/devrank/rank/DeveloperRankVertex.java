package com.yasikstudio.devrank.rank;

import static com.yasikstudio.devrank.rank.Message.*;

import java.io.IOException;
import java.util.Collection;
import java.util.Iterator;
import java.util.Map;

import org.apache.giraph.graph.EdgeListVertex;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.FloatWritable;
import org.apache.hadoop.io.Text;

public class DeveloperRankVertex extends
    EdgeListVertex<Text, UserVertexValue, FloatWritable, Message> {

  private long k;

  @Override
  public void setConf(Configuration conf) {
    this.k = conf.getLong("superstep", 10L);
    super.setConf(conf);
  }

  @Override
  public void compute(Iterator<Message> messages) throws IOException {
    UserVertexValue self = getVertexValue();
    int folVertices = sum(self.getFollowings().values());
    int actVertices = sum(self.getActivities().values());

    if (getSuperstep() > 0) {
      double folDevrank = 0;
      double actDevrank = 0;

      while (messages.hasNext()) {
        Message m = messages.next();
        switch (m.getType()) {
        case FOLLOWING:
          folDevrank += m.getDevrank();
          break;
        case ACTIVITY:
          actDevrank += m.getDevrank();
          break;
        }
      }

      // calculate with PageRank algorithm
      self.setFollowingValue((0.15f / folVertices) + 0.85f * folDevrank);
      self.setActivityValue((0.15f / actVertices) + 0.85f * actDevrank);

      // store my value
      setVertexValue(self);
    }

    if (getSuperstep() < k) {
      sendMsgTo(self.getFollowings(), FOLLOWING, self.getFollowingValue(),
          folVertices);
      sendMsgTo(self.getActivities(), ACTIVITY, self.getActivityValue(),
          actVertices);
    } else {
      voteToHalt();
    }
  }

  private void sendMsgTo(Map<String, Integer> targets, int type, double value,
      int vertices) {
    double v = (vertices != 0) ? (value / vertices) : 0;
    Message msg = new Message(type, v);
    for (String id : targets.keySet()) {
      sendMsg(new Text(id), msg);
    }
  }

  private int sum(Collection<Integer> values) {
    int sum = 0;
    for (int v : values) {
      sum += v;
    }
    return sum;
  }

}
