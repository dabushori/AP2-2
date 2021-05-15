#include "MinCircleAnomalyDetector.h"
#include "timeseries.h"

MinCircleAnomalyDetector::MinCircleAnomalyDetector() {
	// TODO Auto-generated constructor stub

}

MinCircleAnomalyDetector::~MinCircleAnomalyDetector() {
	// TODO Auto-generated destructor stub
}


void MinCircleAnomalyDetector::learnHelper(const TimeSeries& ts,float p/*pearson*/,string f1, string f2,Point** ps){
	Circle cl = findMinCircle(ps,ts.getRowSize());
	correlatedFeatures c;
	c.feature1=f1;
	c.feature2=f2;
	c.corrlation=p;
	c.threshold=cl.radius*1.1; // 10% increase
	c.cx=cl.center.x;
	c.cy=cl.center.y;
	cf.push_back(c);
}

bool MinCircleAnomalyDetector::isAnomalous(float x,float y,correlatedFeatures c){
	return (c.corrlation>=threshold && dist(Point(c.cx,c.cy),Point(x,y))>c.threshold);
}
