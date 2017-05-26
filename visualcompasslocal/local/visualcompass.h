#ifndef VISUAL_COMPASS_H
#define VISUAL_COMPASS_H

#include <alcommon/almodule.h>

#include <alproxies/alvisualcompassproxy.h>
#include <alproxies/almemoryproxy.h>

#include <alerror/alerror.h>

namespace AL{
  // This is a forward declaration of AL:ALBroker which
  // avoids including <alcommon/albroker.h> in this header
  class ALBroker;
}

/**
 * This class inherits AL::ALModule. This allows it to bind methods
 * and be run as a remote executable within NAOqi
 */
class VisualCompass : public AL::ALModule
{
private:
	//Proxies
	boost::shared_ptr<AL::ALVisualCompassProxy> compassProxy;
	boost::shared_ptr<AL::ALMemoryProxy> memoryProxy;

	// De NAOqi, variables para guardar imagenes obtenidas
	AL::ALValue refImage, curImage;

public:
	VisualCompass(boost::shared_ptr<AL::ALBroker> broker, const std::string &name);

	virtual ~VisualCompass();

	/**
	* Overloading ALModule::init().
	* This is called right after the module has been loaded
	*/
	virtual void init();

	// After that you may add all your bind methods.

	float getDesviacionZ();
	int newRefImage();

	//Funciones que podrían implementarse
	//int visualDebug();
	//float getDesviacionY();
	//AL::ALValue getRef();
	//AL::ALValue getCur();
};
#endif // VISUAL_COMPASS_H
