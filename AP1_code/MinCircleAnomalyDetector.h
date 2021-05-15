#ifndef MINCIRCLEANOMALYDETECTOR_H_
#define MINCIRCLEANOMALYDETECTOR_H_

#include "SimpleAnomalyDetector.h"
#include "minCircle.h"

class MinCircleAnomalyDetector : public SimpleAnomalyDetector {
public:
	MinCircleAnomalyDetector();
	virtual ~MinCircleAnomalyDetector();

	virtual void learnHelper(const TimeSeries& ts,float p/*pearson*/,string f1, string f2,Point** ps);
	virtual bool isAnomalous(float x, float y,correlatedFeatures c);
};

#endif /* MINCIRCLEANOMALYDETECTOR_H_ */
