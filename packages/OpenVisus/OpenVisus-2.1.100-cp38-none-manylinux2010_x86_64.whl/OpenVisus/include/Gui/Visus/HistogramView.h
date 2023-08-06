/*-----------------------------------------------------------------------------
Copyright(c) 2010 - 2018 ViSUS L.L.C.,
Scientific Computing and Imaging Institute of the University of Utah

ViSUS L.L.C., 50 W.Broadway, Ste. 300, 84101 - 2044 Salt Lake City, UT
University of Utah, 72 S Central Campus Dr, Room 3750, 84112 Salt Lake City, UT

All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met :

* Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
contributors may be used to endorse or promote products derived from
this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED.IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

For additional information about this project contact : pascucci@acm.org
For support : support@visus.net
-----------------------------------------------------------------------------*/

#ifndef __VISUS_HISTOGRAM_VIEW_H
#define __VISUS_HISTOGRAM_VIEW_H

#include <Visus/Gui.h>
#include <Visus/QCanvas2d.h>
#include <Visus/Histogram.h>

#include <QFrame>
#include <QMouseEvent>

namespace Visus {

////////////////////////////////////////////////////////////////////////
class VISUS_GUI_API HistogramView : public QCanvas2d
{
public:

  VISUS_NON_COPYABLE_CLASS(HistogramView)

  //default constructor
  HistogramView()  {
  }

  //destructor
  virtual ~HistogramView() {
  }

  //setHistogram
  void setHistogram(const Histogram& value) 
  {
    this->histogram=value;
    this->setWorldBox(0.0,0.0,1.0,1.0);
    this->update();
  }

    //resizeEvent
  virtual void resizeEvent(QResizeEvent* evt) override
  {
    QCanvas2d::resizeEvent(evt);
    setHistogram(histogram);
    update();
  }

  //paint
  virtual void paintEvent(QPaintEvent* evt) override
  {
    if (!histogram.getNumBins())
      return;

    QPainter painter(this);
    renderBackground(painter);
    renderGrid(painter);

    auto mylog=[&](double x) {
      return (x==0)? (0) : (1+log(x));
    };

    VisusAssert(getWorldBox().width ==1.0);
    VisusAssert(getWorldBox().height==1.0);

    auto M = 1.25 * (*std::max_element(histogram.bins.begin(), histogram.bins.end()));
    if (!M) 
      return;

    double log_max_bin = mylog(M);

    for (int x=0;x<histogram.getNumBins()-1;x++)
    {
      double x1=(x+0)/(double)(histogram.getNumBins()-1);
      double x2=(x+1)/(double)(histogram.getNumBins()-1);

      double y =histogram.readBin(x)/ M;
      auto log_h = mylog(histogram.readBin(x));

      //log
      painter.setPen(QColor(0,0,0,5));
      painter.setBrush(QColor(173,216,230));
      painter.drawRect(project(QRectF(x1,0,x2-x1,(log_h/log_max_bin))));

      //linear
      painter.setPen(QColor(0,0,0,5));
      painter.setBrush(QColor(100,100,100));
      painter.drawRect(project(QRectF(x1,0,x2-x1,y)));
    }

    {
      auto pos      = getCurrentPos();
      auto screenpos= project(pos);

      //render bin explanation
      double alpha=histogram.getRange().from + pos[0]*histogram.getRange().delta();
      int    bin = histogram.findBin(alpha);
      String description=cstring(
        cnamed("value", alpha),
        cnamed("#bin", cstring(bin,"/", histogram.getNumBins())),
        cnamed("bin_count", histogram.readBin(bin)),
        cnamed("bin_range", cstring(histogram.getBinRange(bin).from,",",histogram.getBinRange(bin).to)));

      painter.setPen(QColor(0,0,0));
      painter.drawText(2,12,description.c_str());

      //render cross
      painter.setPen(QColor(0,0,0,100));
      painter.drawLine(QPointF(0,screenpos[1]),QPointF(this->width(),screenpos[1]));
      painter.drawLine(QPointF(screenpos[0],0),QPointF(screenpos[0],this->height()));
    }

    renderBorders(painter);
  }

private:

  Histogram histogram;

};


} //namespace Visus

#endif //__VISUS_HISTOGRAM_VIEW_H


