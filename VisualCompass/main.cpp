#ifdef VISUALCOMPASS_IS_REMOTE
	# define ALCALL
	#include "visualcompass.h"

	#include <iostream>
	#include <cstdlib>
	//#include <qi/os.hpp>

	#include <alcommon/alproxy.h>
	#include <alcommon/albroker.h>
	#include <alcommon/albrokermanager.h>
	#include <qi/os.hpp>
	#include <alcommon/altoolsmain.h>
#else
	#include "visualcompass.h"

	#include <boost/shared_ptr.hpp>

	#include <alcommon/albroker.h>
	#include <alcommon/albrokermanager.h>

	// when not remote, we're in a dll, so export the entry point
	# ifdef _WIN32
		#  define ALCALL __declspec(dllexport)
	# else
		#  define ALCALL
	# endif
#endif

//
extern "C"
{
	ALCALL int _createModule(boost::shared_ptr<AL::ALBroker> broker)
	{
		// init broker with the main broker instance
		// from the parent executable
		AL::ALBrokerManager::setInstance(broker->fBrokerManager.lock());
		AL::ALBrokerManager::getInstance()->addBroker(broker);

		// create module instances
		AL::ALModule::createModule<VisualCompass>(broker, "VisualCompass");
		return 0;
	}

	ALCALL int _closeModule(  )
	{
		return 0;
	}
} // extern "C" termina


#ifdef VISUALCOMPASS_IS_REMOTE
int main(int argc, char* argv[])
{
	// We will try to connect our broker to a running NAOqi
	int pport = 9559;
	std::string pip = "127.0.0.1";

	// command line parse option
	// check the number of arguments
	if (argc != 1 && argc != 3 && argc != 5)
	{
		std::cerr << "Número incorrecto de argumentos!" << std::endl;
		std::cerr << "Uso: VisualCompass [--pip NAOIP] [--pport NAOPORT]" << std::endl;
		exit(2);
	}

	// if there is only one argument it should be IP or PORT
	if (argc == 3)
	{
		if (std::string(argv[1]) == "--pip")
			pip = argv[2];
		else if (std::string(argv[1]) == "--pport")
			pport = atoi(argv[2]);
		else
		{
			std::cerr << "Número incorrecto de argumentos!" << std::endl;
			std::cerr << "Uso: VisualCompass [--pip NAOIP] [--pport NAOPORT]" << std::endl;
			exit(2);
		}
	}

	// Sepcified IP or PORT for the connection
	if (argc == 5)
	{
		if (std::string(argv[1]) == "--pport"
		&& std::string(argv[3]) == "--pip")
		{
			pport = atoi(argv[2]);
			pip = argv[4];
		}
		else if (std::string(argv[3]) == "--pport"
		&& std::string(argv[1]) == "--pip")
		{
			pport = atoi(argv[4]);
			pip = argv[2];
		}
		else
		{
			std::cerr << "Número incorrecto de argumentos!" << std::endl;
			std::cerr << "Uso: VisualCompass [--pip NAOIP] [--pport NAOPORT]" << std::endl;
			exit(2);
		}
	}

	// Need this to for SOAP serialization of floats to work
	setlocale(LC_NUMERIC, "C");

	// A broker needs a name, an IP and a port:
	const std::string brokerName = "brokerVisionCompass";

	// FIXME: would be a good idea to look for a free port first
	// Encuentra puerto libre
	int brokerPort = 0;

	// listen port of the broker (here an anything)
	const std::string brokerIp = "0.0.0.0";

	// Create your own broker
	boost::shared_ptr<AL::ALBroker> broker;
	try
	{
		broker = AL::ALBroker::createBroker(
			brokerName,
			brokerIp,
			brokerPort,
			pip,
			pport,
			0  // you can pass various options for the broker creation,
			// but default is fine
		);
	} catch(...) {
		std::cerr << "Error al conectar broker a: "
				  << pip
				  << ":"
				  << pport
				  << std::endl;

		AL::ALBrokerManager::getInstance()->killAllBroker();
		AL::ALBrokerManager::kill();

		return 1;
	}

	// Deal with ALBrokerManager singleton (add your broker into NAOqi)
	AL::ALBrokerManager::setInstance(broker->fBrokerManager.lock());
	AL::ALBrokerManager::getInstance()->addBroker(broker);

	// Now it's time to load your module with
	// AL::ALModule::createModule<your_module>(<broker_create>, <your_module>);
	//AL::ALModule::createModule<VisualCompass>(broker, "VisualCompass");
	try{
		// pointer to createModule
		TMainType sig;
		sig = &_createModule;
		// call main
		return ALTools::mainFunction("VisualCompass", argc, argv, sig);
	} catch(const AL::ALError& e){
		std::cout << e.what() << std::endl;
		AL::ALBrokerManager::getInstance()->killAllBroker();
		AL::ALBrokerManager::kill();
	}
	std::cout<<"Termina"<<std::endl;

	return 0;
}
#endif
