#include <stdlib.h>     /* srand, rand */
#include <iostream>   
#include <math.h>
#include <cmath>
#include <tuple>
#include <time.h>       /* time */
#include <list>
#include <vector>
#include <fstream>
#include <string>
#include <iterator> 
#include <cstdlib>
#include <map>
#include <cstring>


using namespace std;

inline float euclideanDistance(tuple<float, float> a, tuple<float, float> b){
    float x1 = get<0>(a);
    float y1 = get<1>(a);
    float x2 = get<0>(b);
    float y2 = get<1>(b);
    float distance = abs(sqrt(pow((x2-x1),2)+pow((y2-y1),2)));
    return distance;
}

inline float manhattanDistance(tuple<float, float> a, tuple<float, float> b){
    float x1 = get<0>(a);
    float y1 = get<1>(a);
    float x2 = get<0>(b);
    float y2 = get<1>(b);
    float distance = abs(x1-y1)+abs(x2-y2);
    return distance;
}

inline float chebyshevDistance(tuple<float, float> a, tuple<float, float> b){
    float x1 = get<0>(a);
    float y1 = get<1>(a);
    float x2 = get<0>(b);
    float y2 = get<1>(b);
    float distance = max(abs(x1-x2),abs(y1-y2));
    return distance;
}

class Circle{
private:
    int rad;
    
public:
    Circle(int r){
        this->rad = r;
    }
    tuple <float, float> randomPointInsideCircle(float centerX, float centerY){
        float pi = 3.142;
        float theta = 2 * pi * rand();
        float p = pow(10,3);
        float r = rad * sqrt( (rand() % int(p) ) / p);
        float x = centerX + r * cos(theta);
        float y = centerY + r * sin(theta);
        return make_tuple(x,y);
    }
    tuple <float, float> randomPointOnCircle(int rad, float centerX, float centerY){
        float pi = 3.142;
        float theta = 2 * pi * rand();
        float r = float(rad);
        float x = centerX + r * cos(theta);
        float y = centerY + r * sin(theta);
        return make_tuple(x,y);
    }
};


class Polygon{
private:
	virtual bool isInside(float X,float Y) =0;
	//virtual tuple <float, float> randomPointInCircle(int rad, float centerX, float centerY, bool onCircumference) = 0;
public:
	virtual void randomPointsToFile (int n) = 0;
	virtual void randomPointsToFile (int distanceD2D , int n) = 0;
};

// functions are overwritten by virtual = dynamic binding
class Hex: public Polygon{
private:
	int circumradius;
	float radius;
    int centerX = 0;
    map<string, tuple <float, float>> verts;
    float v[6][2]; //multi-D array
    Circle *c; // composition
    float (*distance [3]) (tuple<float, float>, tuple<float, float>) = {euclideanDistance ,manhattanDistance ,chebyshevDistance};
    friend void printVerts(Hex *h);
	bool isInside(float X,float Y){
		float x = abs(X);
        float y = abs(Y);
        if (x > this->circumradius or y > this->radius)
            return 0;
        bool cond = (this->circumradius * this->radius - this->circumradius * x - this->circumradius * y)>=0;
        return cond;
	}

	/*tuple <float, float> randomPointInCircle(int rad, float centerX, float centerY, bool onCircumference){
		float pi = 3.142;
		float theta = 2 * pi * rand();
		float r;
		if (onCircumference == 1)
			r = float(rad);
		else {
			float p = pow(10,3);
			r = rad * sqrt( (rand() % int(p) ) / p);
		}
		float x = centerX + r * cos(theta);
        float y = centerY + r * sin(theta);
        return make_tuple(x,y);
	}*/
public:
	Hex(int circumradius){
		srand (time(NULL));
		this->circumradius = circumradius;
        this->radius = circumradius * sqrt(3)/2;
        c = new Circle(circumradius);
        this->v[0][0] = this->circumradius;
        this->v[0][1] = centerX; //shallow copy
        this->v[1][0] = this->circumradius/2;
        this->v[1][1] = sqrt(3)*this->circumradius/2;
        this->v[2][0] = -this->circumradius/2;
        this->v[2][1] = sqrt(3)*this->circumradius/2;
        this->v[3][0] = -this->circumradius;
        this->v[3][1] = centerX; //shallow copy
        this->v[4][0] = -this->circumradius/2;
        this->v[4][1] = sqrt(3)*this->circumradius/2;
        this->v[5][0] = this->circumradius/2;
        this->v[5][1] = -sqrt(3)*this->circumradius/2;
        verts.insert(pair<string, tuple <float, float>>("A", make_tuple(v[0][0],v[0][1])));
        verts.insert(pair<string, tuple <float, float>>("B", make_tuple(v[1][0],v[1][1])));
        verts.insert(pair<string, tuple <float, float>>("C", make_tuple(v[2][0],v[2][1])));
        verts.insert(pair<string, tuple <float, float>>("D", make_tuple(v[3][0],v[3][1])));
        verts.insert(pair<string, tuple <float, float>>("E", make_tuple(v[4][0],v[4][1])));
        verts.insert(pair<string, tuple <float, float>>("F", make_tuple(v[5][0],v[5][1])));
	}
    map<string, tuple <float, float>> getVerts(){
        return verts;
    }
	//2 functions, same name, different paramaters = static binding
	void randomPointsToFile (int n){
		#ifdef DEBUG
	       	cout << "############# 1 point #############" << endl;
 		#endif
		ofstream myfile;
		string fileName;
		fileName = "CUs.txt";
  		myfile.open (fileName);
		list<tuple<float, float>> points;
		for (int i=0; i<n;i++){
			auto p1 = c->randomPointInsideCircle(0, 0);
			float x = get<0>(p1);
			float y = get<1>(p1);
	        while((!isInside(x,y))){
	            p1 = c->randomPointInsideCircle(0, 0);
	            x = get<0>(p1);
				y = get<1>(p1);
	        }
	        points.push_back(p1);
            #ifdef DEBUG
                cout << "(" << x << "," << y << ") " << endl;
            #endif
	    }
	    list<tuple<float, float>> :: iterator it; 
	    for(it = points.begin(); it != points.end(); ++it){
	    	float x = get<0>(*it);
	    	float y = get<1>(*it);
	    	myfile << x << ","<< y << "\n";
	    }
	    myfile.close();
	}
    
     vector<tuple<float, float>> randomPoints(int n){
        #ifdef DEBUG
            cout << "############# 1 point #############" << endl;
        #endif
        vector<tuple<float, float>> points;
        for (int i=0; i<n;i++){
            auto p1 = c->randomPointInsideCircle(0, 0);
            float x = get<0>(p1);
            float y = get<1>(p1);
            while((!isInside(x,y))){
                p1 = c->randomPointInsideCircle(0, 0);
                x = get<0>(p1);
                y = get<1>(p1);
            }
            points.push_back(p1);
            #ifdef DEBUG
                cout << "(" << x << "," << y << ") " << endl;
            #endif
        }
         return points;
    }

	void randomPointsToFile(int distanceD2D , int n){
		#ifdef DEBUG
	       	cout << "############# 2 points (pair) #############" << endl;
 		#endif
		ofstream myfile;
		string fileName;
		fileName = "D2Ds.txt";
  		myfile.open (fileName);
        float *points = new float[n * 2 * 2]; // array [n][2][2] + pointer
        float *p = points; //c++ pointer
		for (int i=0; i<n;i++){
			auto p1 = c->randomPointInsideCircle(0,0);
			float x = get<0>(p1);
			float y = get<1>(p1);
	        while((!isInside(x,y))){
	            p1 = c->randomPointInsideCircle(0, 0);
	            x = get<0>(p1);
				y = get<1>(p1);
	        }
	        *(p+(i*4 + (0*2) + 0)) = get<0>(p1);
            *(p+(i*4 + (0*2) + 1)) = get<1>(p1);
			auto p2 = c->randomPointOnCircle(distanceD2D, x, y);
			float x2 = get<0>(p2);
			float y2 = get<1>(p2);
        	while((!isInside(x2,y2))){
            	p2 = c->randomPointOnCircle(distanceD2D, x, y);
            	x2 = get<0>(p2);
				y2 = get<1>(p2);
			}
            *(p+(i*4 + (1*2) + 0)) = get<0>(p2);
            *(p+(i*4 + (1*2) + 1)) = get<1>(p2);
	        #ifdef DEBUG
                cout << "(" << x << "," << y << ") ";
	        	cout << "(" << x2 << "," << y2 << ")" << endl;
                cout << "Euclidean Distance: "<< (*distance[0])(p1, p2) << endl;
                //cout << "Manhattan Distance: "<< (*distance[1])(p1, p2) << endl;
                //cout << "Chebyshev Distance: "<< (*distance[2])(p1, p2) << endl;
            #endif
	    }
        for (int i=0; i<n*2; i++){
            for(int j=0;j<2;j++){
                float x = *(p+(i*4 + (j*2) + 0));
                float y = *(p+(i*4 + (j*2) + 1));
                myfile << x << ","<< y << "\n";
            }
	    }
	    myfile.close();
	}
    vector<tuple<float, float>> randomPoints(int distanceD2D , int n){
        #ifdef DEBUG
            cout << "############# 2 points (pair) #############" << endl;
        #endif
        vector<tuple<float, float>> points;
        for (int i=0; i<n;i++){
            auto p1 = c->randomPointInsideCircle(0,0);
            float x = get<0>(p1);
            float y = get<1>(p1);
            while((!isInside(x,y))){
                p1 = c->randomPointInsideCircle(0, 0);
                x = get<0>(p1);
                y = get<1>(p1);
            }
            points.push_back(p1);
            auto p2 = c->randomPointOnCircle(distanceD2D, x, y);
            float x2 = get<0>(p2);
            float y2 = get<1>(p2);
            while((!isInside(x2,y2))){
                p2 = c->randomPointOnCircle(distanceD2D, x, y);
                x2 = get<0>(p2);
                y2 = get<1>(p2);
            }
            points.push_back(p2);
            #ifdef DEBUG
                cout << "(" << x << "," << y << ") ";
                cout << "(" << x2 << "," << y2 << ")" << endl;
                cout << "Euclidean Distance: "<< (*distance[0])(p1, p2) << endl;
            #endif
        }
        return points;
    }
};
void printVerts(Hex *h){
    cout << "A: (" << h->v[0][0] << "," << h->v[0][1] << ")" << endl;
    cout << "B: (" << h->v[1][0] << "," << h->v[1][1] << ")" << endl;
    cout << "C: (" << h->v[2][0] << "," << h->v[2][1] << ")" << endl;
    cout << "D: (" << h->v[3][0] << "," << h->v[3][1] << ")" << endl;
    cout << "E: (" << h->v[4][0] << "," << h->v[4][1] << ")" << endl;
    cout << "F: (" << h->v[5][0] << "," << h->v[5][1] << ")" << endl;
}

int main(int argc, char *argv[]){
    int r;
    int distance;
    int n;
    if(argc == 1){
        char *buffer[1];
        char temp_buf[40];
        cout << "radius? " << endl;
        cin >> temp_buf;
        buffer[0] = new char[strlen(temp_buf)+1];
        strcpy(buffer[0], temp_buf);
        r = atoi(buffer[0]);
        cout << "n? " << endl;
        cin >> temp_buf;
        delete [] buffer[0]; // deep copy
        buffer[0] = new char[strlen(temp_buf)+1];
        strcpy(buffer[0], temp_buf);
        n = atoi(buffer[0]);
        cout << "distance? " << endl;
        cin >> temp_buf;
        delete [] buffer[0]; //deep copy
        buffer[0] = new char[strlen(temp_buf)+1];
        strcpy(buffer[0], temp_buf);
        distance = atoi(buffer[0]);
        Hex *g = new Hex(r);
        if (distance >0){
            #ifdef DEBUG
                cout << "radius " << r << endl;
                cout << "number of pairs " << n << endl;
                cout << "distance " << distance << endl;
            #endif
            g->randomPointsToFile(distance,n);
            #ifdef DEBUG
                printVerts(g);
            #endif
        }
        else {
            #ifdef DEBUG
                cout << "radius " << r << endl;
                cout << "number of points " << n << endl;
            #endif
            g->randomPointsToFile(n);
            #ifdef DEBUG
                printVerts(g);
            #endif
        }
        
    } else if (argc == 3){
        r = atoi(argv[1]);
        n = atoi(argv[2]);
        #ifdef DEBUG
            cout << "radius " << r << endl;
            cout << "number of points " << n << endl;
        #endif
        Hex *g = new Hex(r);
        g->randomPointsToFile(n);
        #ifdef DEBUG
            printVerts(g);
        #endif

    } else if (argc == 4){
        r = atoi(argv[1]);
        n = atoi(argv[2]);
        distance = atoi(argv[3]);
        #ifdef DEBUG
            cout << "radius " << r << endl;
            cout << "number of pairs " << n << endl;
            cout << "distance " << distance << endl;
        #endif
        Hex *g = new Hex(r);
        g->randomPointsToFile(distance,n);
        #ifdef DEBUG
            printVerts(g);
        #endif
    }
} 
