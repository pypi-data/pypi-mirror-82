#include <boost/python.hpp>
#include <string>
#include <iostream>
#include <fstream>
#include <vector>

void runslice(std::string directory) {
    std::cout << "Slicing File: " << directory << std::endl;

    std::ifstream infile(directory);
    std::string cube;

    int maxZ = 0;
    std::vector<std::vector<int>> cubelist;

    while(std::getline(infile, cube)){
    	std::vector<int> cubevect;

    	cubevect.push_back(cube.at(0) - '0');
    	cubevect.push_back(cube.at(2) - '0');
    	cubevect.push_back(cube.at(4) - '0');
    	cubelist.push_back(cubevect);
    	
    	if(cube.at(2) > maxZ)
    		maxZ = cube.at(2);
    }

    infile.close();


    std::ofstream gcode;
    gcode.open (directory.erase(directory.length() - 4).append(".gcode"));

    for(int currentZ = 0; currentZ <= maxZ; currentZ++){
    	std::vector<std::vector<int>> cubelayer;
    	for(int index = 0; index < cubelist.size(); index++){
    		if(cubelist.at(index).at(2) == currentZ)
    			cubelayer.push_back(cubelist.at(index));
    	}

		for(int zcoord = (currentZ * 10); zcoord < (currentZ * 10) + 10; zcoord++){
			for(int i = 0; i < cubelayer.size(); i++){

		    	int xcoord = (cubelayer.at(i).at(0) * 10) + 100;
		    	int ycoord = (cubelayer.at(i).at(1) * 10) + 100;

		    	gcode << "; START LAYER " << zcoord - (currentZ * 10) << std::endl;
		    	
		    	gcode << "G1 X" << xcoord << " Y" << ycoord << std::endl;
		    	gcode << "G1 Z" << zcoord << std::endl;
		    	
		    	for(; ycoord < (cubelayer.at(i).at(1) * 10) + 110; ycoord+=2){
		    		gcode << "G1 X" << xcoord + 10 << " Y" << ycoord << std::endl;
		    		gcode << "G1 X" << xcoord + 10 << " Y" << ycoord + 1 << std::endl;
		    		gcode << "G1 X" << xcoord << " Y" << ycoord + 1<< std::endl;
		    		gcode << "G1 X" << xcoord << " Y" << ycoord + 2<< std::endl;
		    	}
		    	gcode << "G1 Z" << zcoord + 3 << std::endl;
	    		gcode << "; END LAYER " << zcoord - (currentZ * 10) << std::endl;
	    	}
    	}
    }

    gcode.close();
}

BOOST_PYTHON_MODULE(_slice) {
    using namespace boost::python;

    def("runslice", runslice);
}