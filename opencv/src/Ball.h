//============================================================================
// Name : Ball.h
// Description : Outlines the Ball object.
//============================================================================

#ifndef BALL_H_
#define BALL_H_

#include "Object.h"
#include "zhelpers.hpp"

class Ball: public Object {
  public:

    // Constructor
    Ball();

    // Destructor
    virtual ~Ball();

    // Ball Methods
    void calibrateBall(cv::VideoCapture capture);
    std::string trackFilteredBall(cv::Mat threshold, cv::Mat HSV, cv::Mat &cameraFeed);
    void drawBall(cv::Mat &frame);
};

#endif /* BALL_H_ */
