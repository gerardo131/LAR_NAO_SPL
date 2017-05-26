#include "visualcompass.h"

/** CONSTRUCTOR **/
VisualCompass::VisualCompass(boost::shared_ptr<AL::ALBroker> broker,
                   const std::string& name) : AL::ALModule(broker, name)
{
  // Describe the module here. This will appear on the webpage
  setModuleDescription("Módulo de brújula usando visión.");

  /**
   * Define callable methods with their descriptions:
   * This makes the method available to other cpp modules
   * and to python.
   * The name given will be the one visible from outside the module.
   * This method has no parameters or return value to describe
   * functionName(<method_name>, <class_name>, <method_description>);
   * BIND_METHOD(<method_reference>);
   */
  //functionName("printHello", getName(), "Print hello to the world");
  //BIND_METHOD(VisualCompass::printHello);

  /**
   * addParam(<attribut_name>, <attribut_descrption>);
   * This enables to document the parameters of the method.
   * It is not compulsory to write this line.
   */
  //functionName("printWord", getName(), "Print a given word.");
  //addParam("word", "The word to be print.");
  //BIND_METHOD(VisualCompass::printWord);

  /**
   * setReturn(<return_name>, <return_description>);
   * This enables to document the return of the method.
   * It is not compulsory to write this line.
   */
  //functionName("returnTrue", getName(), "Just return true");
  //setReturn("boolean", "return true");
  //BIND_METHOD(VisualCompass::returnTrue);

  // If you had other methods, you could bind them here...
  functionName("getDesviacionZ", getName(), "Regresa la desviación con respecto a Z");
  BIND_METHOD(VisualCompass::getDesviacionZ);

  //functionName("visualDebug", getName(), "Muestra tres ventanas para observar lo que ve el robot");
  //BIND_METHOD(VisualCompass::visualDebug);

  functionName("newRefImage", getName(), "Crea nueva imagen de referencia");
  BIND_METHOD(VisualCompass::newRefImage);

  /**
   * Bound methods can only take const ref arguments of basic types,
   * or AL::ALValue or return basic types or an AL::ALValue.
   */
}

/** DESTRUCTOR **/
VisualCompass::~VisualCompass()
{
	std::cout<<"Destruyendo y quitando la suscripción"<<std::endl;
	compassProxy->unsubscribe("VisualCompass");
}

/**
* Init is called just after construction.
* Do something or not
*/
void VisualCompass::init()
{
	try { // Creating proxy to ALVisualCompass.
		compassProxy = boost::shared_ptr<AL::ALVisualCompassProxy>(new AL::ALVisualCompassProxy);
		memoryProxy = boost::shared_ptr<AL::ALMemoryProxy>(new AL::ALMemoryProxy);
	} catch (const AL::ALError& e) {
		//std::cerr << "Could not create proxies: " << e.what() << std::endl;
	}

	// Reference will be set each time the module is subscribed.
	compassProxy->enableReferenceRefresh(false);

	// Image resolution is QVGA (320x240).
	compassProxy->setResolution(1);

	// Escoger la cámara de arriba con id=0
	compassProxy->setActiveCamera(0);

	//compassProxy->subscribe("VisualCompass");
}

float VisualCompass::getDesviacionZ(){
	AL::ALValue deviation;

  // Escoger la cámara de arriba con id=0
	compassProxy->setActiveCamera(0);

	compassProxy->subscribe("VisualCompass");
	//std::cout<<"Suscrito"<<std::endl;
	//compassProxy->pause(false);
	//std::cout<<"pause = false\n";

	// Get the deviation information from the ALMemory event.
	try {
		deviation = memoryProxy->getData("VisualCompass/Deviation");
	}
	catch (const AL::ALError& e) {
	   //std::cerr << "Could not create proxy: " << e.what() << std::endl;
	}

	float wz = deviation[0][1];

	// std::cout<<"Posición del robot en WORLD_SPACE cuando se toma la foto: \n"
	// 		 << " X: "<< deviation[1][0]
	// 		 << " Y: "<< deviation[1][1]
	// 		 << " Theta: "<< deviation[1][2]
	// 		 << std::endl
	// 		 << "Desviación con respecto a Z, en grados: "
	// 		 << wz * 180.0f / 3.14159f
	// 		 << std::endl;

	compassProxy->unsubscribe("VisualCompass");
	//std::cout<<"No suscrito\n"<<std::endl;
	//compassProxy->pause(true);
	//std::cout<<"pause = true\n"<<std::endl;

	return wz;
}

int VisualCompass::newRefImage(){
  // Escoger la cámara de arriba con id=0
  compassProxy->setActiveCamera(0);

  // Reference will be set each time the module is subscribed.
  compassProxy -> enableReferenceRefresh(true);

  compassProxy->subscribe("VisualCompass");
  std::cout<<"pause = true\n"<<std::endl;

  compassProxy->unsubscribe("VisualCompass");
	std::cout<<"pause = false\n"<<std::endl;

  compassProxy -> enableReferenceRefresh(false);

  return 0;
}

/*
int VisualCompass::visualDebug(){
  // Escoger la cámara de arriba con id=0
  compassProxy->setActiveCamera(0);

  // Initialize image containers for display.
  cv::Mat referenceImage = cv::Mat::zeros(240, 320, CV_8UC1);
  AL::ALValue refImage, curImage;
  cv::Mat currentImage = cv::Mat::zeros(240, 320, CV_8UC1);
  cv::Mat matchImage = cv::Mat::zeros(480, 320, CV_8UC1);

  AL::ALValue deviation;
  AL::ALValue matchInfo;
  cv::Mat roi;

  while (true){
    char key = cv::waitKey(50);
    // Esc key to exit.
    if (cv::waitKey(50) == 27) {
      break;
    }

    refImage = compassProxy->getReferenceImage();
    referenceImage.data = (uchar*) refImage[6].GetBinary();

    // Retrieve the current image for display.
    curImage = compassProxy->getCurrentImage();
    currentImage.data = (uchar*) curImage[6].GetBinary();

    // Get the deviation information from the ALMemory event.
    try {
      deviation = memoryProxy->getData("VisualCompass/Deviation");
      matchInfo = memoryProxy->getData("VisualCompass/Match");
    }
    catch (const AL::ALError& e) {
      std::cout << e.what() << std::endl;
    }

    float wy = deviation[0][0], wz = deviation[0][1];
    // Convert it to degrees.
    wz = wz * 180.0f / 3.14159f;
    wy = wy * 180.0f / 3.14159f;
    // Display it on the image.
    char buffer [100];
    sprintf(buffer, "Wz: %.2f deg, Wy: %.2f deg", wz, wy);
    cv::putText(currentImage, buffer, cv::Point(10,30), CV_FONT_HERSHEY_PLAIN,
    1.0f, cv::Scalar(255), 2);

    roi = matchImage(cv::Rect(0,0, 320, 240));
    referenceImage.copyTo(roi);
    roi = matchImage(cv::Rect(0, 240, 320, 240));
    currentImage.copyTo(roi);

    for (int i = 0; i < static_cast<int>(matchInfo[3][1].getSize()); ++i){
      AL::ALValue match = matchInfo[2][matchInfo[3][1][i]];
      AL::ALValue refKp = matchInfo[0][match[0]];
      cv::Point ref = cv::Point((float) refKp[0][0], (float) refKp[0][1]);
      AL::ALValue curKp = matchInfo[1][match[1]];
      cv::Point cur = cv::Point((float) curKp[0][0], (float) curKp[0][1]);
      cur.y += 240;
      cv::line(matchImage, cur, ref, cv::Scalar(255));
      cv::circle(matchImage, ref, (float) refKp[1], cv::Scalar(255));
      cv::circle(matchImage, cur, (float) curKp[1], cv::Scalar(255));
    }
    cv::imshow("Reference image", referenceImage);
    cv::imshow("Current image", currentImage);
    cv::imshow("Match", matchImage);
  }
  return 0;
}
*/

/*
AL::ALValue VisualCompass::getRef(){
	compassProxy->pause(false);

	// Obtener imagen de referencia
	refImage = compassProxy->getReferenceImage();

	compassProxy->pause(true);

	return refImage;
}

AL::ALValue VisualCompass::getCur(){

	// Retrieve the current image for display.
	curImage = compassProxy->getCurrentImage();

	return curImage;
}

void VisualCompass::ver(){

}
*/

/*
 * No se ocupa en el penal, porque se acomoda con respecto
 * a la pelota roja en la dirección Y.
 */
/*
float VisualCompass::getDesviacionY(){
	AL::ALValue deviation;
	//compassProxy->subscribe("VisualCompass");
	compassProxy->pause(false);
	std::cout<<"pause = false"<<std::endl;
	float wy = 0.0;

	// Get the deviation information from the ALMemory event.
	try {
		deviation = memoryProxy->getData("VisualCompass/Deviation");
		wy = deviation[0][0];
	}
	catch (const AL::ALError& e) {
		std::cerr << "Could not create proxy: " << e.what() << std::endl;
	}

	//compassProxy->unsubscribe("VisualCompass");
	compassProxy->pause(true);
	std::cout<<"pause = true"<<std::endl;

	return wy;
}
*/
